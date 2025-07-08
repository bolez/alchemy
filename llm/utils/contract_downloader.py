from llm.models.data_contract import DataContract
from typing import Dict, Any
import yaml
import os

def download_contract_in_yaml(contract: Dict[str, Any]) -> DataContract:
    """
    Parses a validated data contract dictionary into a Pydantic model,
    then saves it as a YAML file.
    """
    print(type(contract), contract)
    file_path = "data_contract1.yaml"
    contract_data = DataContract(**{
        "version": "1.0.0",  # Add version if missing
        **contract
    })
    
    yaml_output = yaml.dump(contract_data.model_dump(), sort_keys=False, allow_unicode=True)

    with open(file_path, "w") as f:
        f.write(yaml_output)
    
    return {"status": "success", "file_path": os.path.abspath(file_path)}


def save_markdown_tool(input_data: Dict[str, Any]) -> dict:
    """
    save markdown contract into file
    """
    
    file_name = "contract1.md"
    try:
        # Replace literal '\n' with real newlines if needed
        cleaned_content = input_data.encode("utf-8").decode("unicode_escape")

        with open(file_name, "w", encoding="utf-8") as f:
            f.write(cleaned_content)

        return {
            "status": "success",
            "file_path": os.path.abspath(file_name)
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
    }