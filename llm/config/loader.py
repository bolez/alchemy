import yaml


def load_config(path="llm/config/llm_config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_graph_config(path="llm/config/graph_config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)
