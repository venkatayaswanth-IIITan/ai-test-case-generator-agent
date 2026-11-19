
import pandas as pd


def export_to_csv(test_cases):

    rows = []

    for case in test_cases:

        rows.append({
            "Test Case ID": case["test_case_id"],
            "Scenario": case["scenario_type"],
            "Title": case["title"],
            "Preconditions": case["preconditions"],
            "Steps": " | ".join(case["steps"]),
            "Test Data": case["test_data"],
            "Expected Result": case["expected_result"],
            "Priority": case["priority"]
        })

    df = pd.DataFrame(rows)

    return df.to_csv(index=False).encode("utf-8")
