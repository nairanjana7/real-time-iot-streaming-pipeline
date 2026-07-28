from backend.services.ml_service import predict_machine

sample = {
    "Type": "M",
    "Air temperature [K]": 298.3,
    "Process temperature [K]": 308.3,
    "Rotational speed [rpm]": 1379,
    "Torque [Nm]": 48.0,
    "Tool wear [min]": 181
}

report = predict_machine(sample)

print(report)
