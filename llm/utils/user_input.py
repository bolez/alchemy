import subprocess
import tempfile
import os

def add_watermark(contract: dict, agent: str) -> dict:
    contract["_created_by"] = agent
    return contract


def remove_watermark(contract: dict) -> dict:
    contract.pop("_created_by", None)
    return contract


def get_user_input_via_editor(initial_text: str = "") -> str:
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode='w', encoding='utf-8') as tf:
        tf.write(initial_text)
        temp_filename = tf.name

    editor = os.environ.get("EDITOR", "vi")
    subprocess.call([editor, temp_filename])

    with open(temp_filename, "r", encoding='utf-8') as tf:
        updated_text = tf.read()

    os.unlink(temp_filename) 
    return updated_text


