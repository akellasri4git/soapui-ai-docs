import json

class TestCaseLLMInputBuilder:
    """
    Converts enriched JSON test case data into a SMALL,
    LLM-friendly prompt payload.
    """

    @staticmethod
    def build(test_suite_name, test_case):
        return {
            "test_suite": test_suite_name,
            "test_case": test_case["name"],
            "enabled": test_case.get("enabled", True),
            "endpoints": sorted(set(test_case.get("endpoints", []))),
            "operations": sorted(set(test_case.get("operations", []))),
            "queues": sorted(set(test_case.get("queues", []))),
            "steps": [
                {
                    "name": step.get("name"),
                    "type": step.get("type"),
                    "details": step.get("details", "")
                }
                for step in test_case.get("steps", [])
            ],
            "assertions": test_case.get("assertions", [])
        }

    @staticmethod
    def to_prompt(payload: dict) -> str:
        return f"""
Explain the following SoapUI test case in simple language.

Test Suite:
{payload['test_suite']}

Test Case:
{payload['test_case']} (Enabled: {payload['enabled']})

Endpoints Used:
{payload['endpoints']}

Operations:
{payload['operations']}

Queues:
{payload['queues']}

Test Steps:
{json.dumps(payload['steps'], indent=2)}

Assertions / Validations:
{json.dumps(payload['assertions'], indent=2)}

Explain clearly:
1. What this test case does
2. What it validates
3. Why this test is important
"""
