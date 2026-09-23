import requests
import random
import time

API_URL = "http://127.0.0.1:8001/predict"

MACHINE_TYPES = {
    "M001": "M",
    "M002": "M",
    "L001": "L",
    "H001": "H",
}

def generate_reading(machine_id):
    machine_type = MACHINE_TYPES[machine_id]

    air_temp = round(random.uniform(295, 304), 1)
    process_temp = round(air_temp + random.uniform(8, 12), 1)
    rotational_speed = round(random.uniform(1200, 2000), 1)
    torque = round(random.uniform(20, 60), 1)
    tool_wear = round(random.uniform(0, 250), 1)

    return {
        "machine_id": machine_id,
        "air_temperature": air_temp,
        "process_temperature": process_temp,
        "rotational_speed": rotational_speed,
        "torque": torque,
        "tool_wear": tool_wear,
        "type": machine_type,
    }

def run_simulation(num_readings=10, delay_seconds=2):
    machine_ids = list(MACHINE_TYPES.keys())

    for i in range(num_readings):
        machine_id = random.choice(machine_ids)
        reading = generate_reading(machine_id)

        response = requests.post(API_URL, json=reading)

        if response.status_code == 200:
            result = response.json()
            print(f"[{i+1}] {machine_id} -> risk={result['risk_level']}, "
                  f"probability={result['probability']}")
        else:
            print(f"[{i+1}] {machine_id} -> ERROR {response.status_code}: {response.text}")

        time.sleep(delay_seconds)

if __name__ == "__main__":
    run_simulation(num_readings=10, delay_seconds=2)