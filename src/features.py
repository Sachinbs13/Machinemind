def engineer_features(air_temperature, process_temperature, rotational_speed,
                       torque, tool_wear, machine_type):
    power = torque * rotational_speed
    temp_diff = process_temperature - air_temperature
    strain = tool_wear * torque

    return {
        "Air temperature [K]": air_temperature,
        "Process temperature [K]": process_temperature,
        "Rotational speed [rpm]": rotational_speed,
        "Torque [Nm]": torque,
        "Tool wear [min]": tool_wear,
        "Power [W]": power,
        "Temp difference [K]": temp_diff,
        "Strain [Nm·min]": strain,
        "Type_L": 1 if machine_type == "L" else 0,
        "Type_M": 1 if machine_type == "M" else 0,
    }