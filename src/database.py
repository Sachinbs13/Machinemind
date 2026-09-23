import sqlite3

DB_PATH = "../data/machinemind.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS machines (
            machine_id TEXT PRIMARY KEY,
            type TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id TEXT NOT NULL,
            air_temperature REAL,
            process_temperature REAL,
            rotational_speed REAL,
            torque REAL,
            tool_wear REAL,
            recorded_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (machine_id) REFERENCES machines (machine_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenance_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id TEXT NOT NULL,
            predicted_failure INTEGER,
            risk_level TEXT,
            probability REAL,
            recommended_action TEXT,
            predicted_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (machine_id) REFERENCES machines (machine_id)
        )
    """)

    conn.commit()
    conn.close()

def log_prediction(machine_id, machine_type, air_temperature, process_temperature,
                    rotational_speed, torque, tool_wear,
                    predicted_failure, risk_level, probability, recommended_action):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO machines (machine_id, type) VALUES (?, ?)",
        (machine_id, machine_type)
    )

    cursor.execute("""
        INSERT INTO sensor_data
        (machine_id, air_temperature, process_temperature, rotational_speed, torque, tool_wear)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (machine_id, air_temperature, process_temperature, rotational_speed, torque, tool_wear))

    cursor.execute("""
        INSERT INTO maintenance_records
        (machine_id, predicted_failure, risk_level, probability, recommended_action)
        VALUES (?, ?, ?, ?, ?)
    """, (machine_id, predicted_failure, risk_level, probability, recommended_action))

    conn.commit()
    conn.close()

def get_recent_predictions(limit=20):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, machine_id, predicted_failure, risk_level, probability,
               recommended_action, predicted_at
        FROM maintenance_records
        ORDER BY predicted_at DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

if __name__ == "__main__":
    initialize_database()
    print("Database initialized at", DB_PATH)