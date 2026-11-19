
import json
import re
from agent import run_agent


REQUIRED_FIELDS = [
    "scenario_type",
    "title",
    "preconditions",
    "steps",
    "test_data",
    "expected_result",
    "priority"
]


def generate_test_cases(requirement):

    if not requirement.strip():
        raise ValueError("Please enter a requirement.")

    response = run_agent(requirement)

    response = response.strip()

    response = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        response,
        flags=re.IGNORECASE
    )

    data = json.loads(response)

    if not isinstance(data, dict):
        raise ValueError("Invalid AI response.")

    if "test_cases" not in data:
        raise ValueError("Test cases are missing.")

    cases = data["test_cases"]

    if not isinstance(cases, list) or not cases:
        raise ValueError("No valid test cases generated.")

    valid_cases = []

    for index, case in enumerate(cases, start=1):

        if not isinstance(case, dict):
            continue

        if not all(field in case for field in REQUIRED_FIELDS):
            continue

        if not isinstance(case["steps"], list):
            continue

        if not all(
            isinstance(step, str) and step.strip()
            for step in case["steps"]
        ):
            continue

        if case["priority"] not in ["High", "Medium", "Low"]:
            continue

        if case["scenario_type"] not in [
            "Positive", "Negative", "Edge"
        ]:
            continue

        if not all(
            isinstance(case[field], str)
            for field in REQUIRED_FIELDS
            if field != "steps"
        ):
            continue

        case["test_case_id"] = f"TC-{index:02d}"

        valid_cases.append(case)

    if not valid_cases:
        raise ValueError("AI did not generate valid test cases.")

    data["test_cases"] = valid_cases

    return data
