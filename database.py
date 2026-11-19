
import sqlite3
import json

DB_NAME = "test_cases.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requirements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requirement TEXT NOT NULL,
            feature_summary TEXT,
            assumptions TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requirement_id INTEGER,
            test_case_id TEXT,
            scenario_type TEXT,
            title TEXT,
            preconditions TEXT,
            steps TEXT,
            test_data TEXT,
            expected_result TEXT,
            priority TEXT,
            FOREIGN KEY(requirement_id)
            REFERENCES requirements(id)
        )
    """)

    conn.commit()
    conn.close()


def save_results(requirement, data):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO requirements
        (requirement, feature_summary, assumptions)
        VALUES (?, ?, ?)
    """, (
        requirement,
        data.get("feature_summary", ""),
        json.dumps(data.get("assumptions", []))
    ))

    requirement_id = cursor.lastrowid

    for case in data["test_cases"]:

        cursor.execute("""
            INSERT INTO test_cases (
                requirement_id,
                test_case_id,
                scenario_type,
                title,
                preconditions,
                steps,
                test_data,
                expected_result,
                priority
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            requirement_id,
            case["test_case_id"],
            case["scenario_type"],
            case["title"],
            case["preconditions"],
            json.dumps(case["steps"]),
            case["test_data"],
            case["expected_result"],
            case["priority"]
        ))

    conn.commit()
    conn.close()


def get_history():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, requirement, feature_summary
        FROM requirements
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_saved_results(requirement_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            test_case_id,
            scenario_type,
            title,
            preconditions,
            steps,
            test_data,
            expected_result,
            priority
        FROM test_cases
        WHERE requirement_id = ?
    """, (requirement_id,))

    rows = cursor.fetchall()
    conn.close()

    results = []

    for row in rows:
        results.append({
            "test_case_id": row[0],
            "scenario_type": row[1],
            "title": row[2],
            "preconditions": row[3],
            "steps": json.loads(row[4]),
            "test_data": row[5],
            "expected_result": row[6],
            "priority": row[7]
        })

    return results
