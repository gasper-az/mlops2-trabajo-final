import random
import time
import requests

URL = "http://localhost:8080/predict"
REQUEST_DELAY = 0.3
NORMAL_SAMPLES = 100
DRIFT_SAMPLES = 200
POISONING_SAMPLES = 200


def normal_sample():
    return {
        "alcohol": random.normalvariate(13.0, 0.7),
        "malic_acid": random.normalvariate(2.0, 1.0),
        "ash": random.normalvariate(2.4, 0.3),
        "alcalinity_of_ash": random.normalvariate(17, 3),
        "magnesium": random.normalvariate(100, 15),
        "total_phenols": random.normalvariate(2.5, 0.5),
        "flavanoids": random.normalvariate(2.3, 0.7),
        "nonflavanoid_phenols": random.normalvariate(0.3, 0.1),
        "proanthocyanins": random.normalvariate(1.5, 0.5),
        "color_intensity": random.normalvariate(5.0, 1.0),
        "hue": random.normalvariate(1.0, 0.2),
        "od280_od315": random.normalvariate(3.0, 0.4),
        "proline": random.normalvariate(750, 300),
    }

def drift_sample():
    s = normal_sample()
    s["alcohol"] += 2.0
    s["color_intensity"] += 3.0
    s["proline"] += 400
    return s

def poisoning_sample():
    return {
        "alcohol": 15.5,
        "malic_acid": 3.0,
        "ash": 3.0,
        "alcalinity_of_ash": 22.0,
        "magnesium": 140,
        "total_phenols": 1.2,
        "flavanoids": 0.8,
        "nonflavanoid_phenols": 0.6,
        "proanthocyanins": 0.9,
        "color_intensity": 11.0,
        "hue": 0.4,
        "od280_od315": 1.2,
        "proline": 1500
    }

def send_batch(label, generator, count):
    for i in range(count):
        payload = generator()
        try:
            response = requests.post(
                URL,
                json=payload,
                timeout=3
            )
            print(f"{label} #{i+1}: {response.status_code}")
        except Exception as e:
            print(f"{label} #{i+1}: ERROR - {e}")
        time.sleep(REQUEST_DELAY)

if __name__ == "__main__":
    send_batch("NORMAL", normal_sample, NORMAL_SAMPLES)
    send_batch("DRIFT", drift_sample, DRIFT_SAMPLES)
    send_batch("POISONING", poisoning_sample, POISONING_SAMPLES)

    print("Trafico generado satisfactoriamente!!!!")