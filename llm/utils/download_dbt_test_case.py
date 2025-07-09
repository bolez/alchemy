from typing import Dict, List, Any
from collections import defaultdict
import json
import yaml


def download_dbt_yaml(tests_data: Dict[str, List[Dict[str, Any]]], file_path: str = "schema.yml") -> None:
    """
    Convert DBT tests into a dbt-compatible YAML format and save to file.

    Args:
        tests_data: Dictionary with key 'tests' and value as a list of test definitions.
        file_path: Output YAML file path. Default is 'schema.yml'.
    """

    # Group by column
    columns_dict = defaultdict(lambda: {"description": "", "tests": []})

    for test in tests_data.get("tests", []):
        col_name = test["column_name"]
        description = test.get("description", "")
        test_name = test["test_name"]
        params = None
        try:
            params = eval(test["test_parameters"])
            params.pop("column_name", None)

        except (json.JSONDecodeError, Exception) as e:
            print(f"Skipping malformed test parameters for column '{col_name}': {e}")
            # continue  # skip malformed JSON

        # Remove duplicate column_name from test parameters

        # Build the test block
        test_entry = {test_name: {"column_name": col_name, **params}} if params else {test_name: {"column_name": col_name}}

        columns_dict[col_name]["description"] = description
        columns_dict[col_name]["tests"].append(test_entry)

    # Convert to YAML structure
    yaml_structure = {
        "models": [
            {   "model_name": tests_data.get("model_name", "default_model"),
                "description": tests_data.get("model_discription", "No description provided"),
                "columns": [
                    {
                        "name": col,
                        "description": data["description"],
                        "tests": data["tests"]
                    } for col, data in columns_dict.items()
                ]
            }
        ],
        "version": 2

    }

    # Save as YAML file
    with open(file_path, "w") as f:
        yaml.dump(yaml_structure, f, sort_keys=False)

    print(f"YAML file saved to {file_path}")
