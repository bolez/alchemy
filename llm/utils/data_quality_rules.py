
import yaml


def retrieve_rule_examples() -> str:
    """
    Load rule types with their descriptions and examples from YAML to guide the LLM.
    """
    all_rules = []
    with open("llm/utils/test_cases.yaml", "r") as f:
        rules_yaml = yaml.safe_load(f)
        all_rules = list(rules_yaml.keys())
    result_blocks = []
    for rule, detailes in rules_yaml.items():
        rule_type = rule
        desc = detailes.get("description", "")
        example = detailes.get("example", "")

        result_blocks.append(
            f"Rule Type: {rule_type}\nDescription: {desc}\nExample:\n{yaml.dump(example)}"
        )
    all_rules_with_example = "\n\n".join(result_blocks)
    return all_rules_with_example, all_rules


rule_refrences, all_rules = retrieve_rule_examples()
