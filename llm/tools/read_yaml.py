from typing import Dict, Any
from llm.tools.decorators import register_tool
import yaml


@register_tool("system")
def read_yml_file(file_path) -> Dict[str, Any]:
    """
        convert yaml file to dict

    Args:
        file_path (_type_): yaml file path

    Returns:
        Dict[str, Any]: yaml file content in dict format
    """  
    print(f"Reading YAML file: {file_path}")
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
        return {"data": data}