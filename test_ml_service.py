from backend.services.ml_service import predict_machine


def test_predict_machine():
    sample = {
        "type": "M",
        "air_temperature": 298.3,
        "process_temperature": 308.3,
        "rotational_speed": 1379,
        "torque": 48.0,
        "tool_wear": 181,
    }

    report = predict_machine(sample)

    assert report is not None
    assert "prediction" in report
    assert report["prediction"] in ["Failure", "Healthy"]
