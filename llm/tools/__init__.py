import os
import importlib

exclude = ["__init__.py", "decorators.py", "tool_node.py", "tool_registry.py"]
def load_all_tools():
    tools_dir = os.path.dirname(__file__)
    for file in os.listdir(tools_dir):
        if file.endswith(".py") and file not in exclude:
            module_name = f"llm.tools.{file[:-3]}"
            importlib.import_module(module_name)
