from llm.models.data_contract import DataContract
from typing import Dict, Any
import yaml
import os
from llm.utils.s3 import S3Media
s3_media = S3Media()

def download_contract_in_yaml(domain: str, contract: Dict[str, Any]) -> DataContract:
    """
    Parses a validated data contract dictionary into a Pydantic model,
    then saves it as a YAML file.
    """
    # os.makedirs(f"contracts/{domain}", exist_ok=True)

    file_path = f"contracts/{domain}/data_contract.yaml"
    contract_data = DataContract(**{
        "version": "1.0.0",
        **contract
    })
    
    # yaml_output = yaml.dump(contract_data.model_dump(), sort_keys=False, allow_unicode=True)

    # with open(file_path, "w") as f:
    #     f.write(yaml_output)
    # s3_key = f"contracts/{domain}/{file_path}"
    s3_url = s3_media.upload_file(contract_data.model_dump(), file_path)
    
    return {"status": "success", "file_path": s3_url}


def save_markdown_tool(domain: str, input_data: Dict[str, Any]) -> dict:
    """
    save markdown contract into file
    """
    # os.makedirs(f"contracts/{domain}", exist_ok=True)
    file_name = f"contracts/{domain}/data_contract.md"
    try:
        cleaned_content = input_data.encode("utf-8").decode("unicode_escape").strip()

        if cleaned_content.startswith("```markdown") and cleaned_content.endswith("```"):
            cleaned_content = "\n".join(cleaned_content.splitlines()[1:-1]).strip()

        # with open(file_name, "w", encoding="utf-8") as f:
        #     f.write(cleaned_content)
        s3_url = s3_media.upload_file(cleaned_content, file_name)

        return {
            "status": "success",
            "file_path": s3_url
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
    }