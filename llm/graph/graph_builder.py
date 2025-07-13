from llm.graph.nodes import CORE_NODE_REGISTRY, AGENT_CLASS_REGISTRY, FUNCTION_NODE_REGISTRY
from llm.models.agent_state import AgentState
from llm.config.loader import load_graph_config
from langgraph.graph import StateGraph, START, END


class AgentGraphBuilder:
    def __init__(self, config=None):
        self.config = config or load_graph_config()
        self.llm_model = self.config["llm"]
        self.agents = self.config["agents"]
        self.core_nodes = self.config.get("core_nodes", [])
        self.edges = self.config.get("edges", [])
        self.graph_builder = StateGraph(AgentState)

    def _load_core_nodes(self):
        for node in self.core_nodes:
            name = node["name"]
            class_name = node["class"]
            if class_name not in CORE_NODE_REGISTRY:
                raise ValueError(f"Core node class '{class_name}' not registered.")
            self.graph_builder.add_node(name, CORE_NODE_REGISTRY[class_name](self.llm_model))

    def _load_agent_nodes(self):
        for agent in self.agents:
            if agent_class := AGENT_CLASS_REGISTRY.get(agent):
                self.graph_builder.add_node(agent, agent_class(model=self.llm_model))
            elif function_node := FUNCTION_NODE_REGISTRY.get(agent):
                self.graph_builder.add_node(agent, function_node)
            else:
                raise ValueError(f"Agent '{agent}' not found in registry.")

    def _handle_condition(self, condition_type):
        if condition_type == "should_continue":
            def should_continue(state):
                last_msg = state["messages"][-1]
                return "continue" if getattr(last_msg, "tool_calls", []) else "respond"
            return should_continue
        if condition_type == "next_agent":
            return lambda state: state.get("next_agent", "FINISH")
        raise ValueError(f"Unknown condition type: {condition_type}")

    def _resolve_node(self, node_name: str):
        if node_name == "START":
            return START
        elif node_name == "END":
            return END
        return node_name

    def _load_edges(self):
        for edge in self.edges:
            src = self._resolve_node(edge["from"])
            if edge.get("condition"):
                cond_fn = self._handle_condition(edge["condition"]["type"])
                paths = {key: self._resolve_node(val) for key, val in edge["condition"]["paths"].items()}
                self.graph_builder.add_conditional_edges(src, cond_fn, paths)
            else:
                tgt = self._resolve_node(edge["to"])
                self.graph_builder.add_edge(src, tgt)
        

    def compile(self, checkpointer=None):
        self._load_core_nodes()
        self._load_agent_nodes()
        self._load_edges()
        return self.graph_builder.compile(checkpointer=checkpointer)
