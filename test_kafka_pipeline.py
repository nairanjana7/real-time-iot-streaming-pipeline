from consumers.ml_consumer import normalize_telemetry


def test_normalize_telemetry():
    kafka_data = {
        "Type": "M",
        "Air temperature [K]": 298.3,
        "Process temperature [K]": 308.3,
        "Rotational speed [rpm]": 1379,
        "Torque [Nm]": 48.0,
        "Tool wear [min]": 181,
    }

    result = normalize_telemetry(kafka_data)

    assert result == {
        "type": "M",
        "air_temperature": 298.3,
        "process_temperature": 308.3,
        "rotational_speed": 1379,
        "torque": 48.0,
        "tool_wear": 181,
    }


def test_normalize_telemetry_rejects_missing_field():
    kafka_data = {
        "Type": "M",
        "Air temperature [K]": 298.3,
        "Process temperature [K]": 308.3,
        "Rotational speed [rpm]": 1379,
        "Torque [Nm]": 48.0,
    }

    try:
        normalize_telemetry(kafka_data)
        assert False, "Expected missing field to raise KeyError"
    except KeyError as e:
        assert e.args[0] == "Tool wear [min]"
