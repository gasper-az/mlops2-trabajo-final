import random
import time
import requests

URL = "http://localhost:8080/predict"

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
        "color_intensity": random.normalvariate(5.1, 1.0),
        "hue": random.normalvariate(1.0, 0.2),
        "od280_od315": random.normalvariate(3.0, 0.4),
        "proline": random.normalvariate(750, 300),
    }

def drift_sample():
    s = normal_sample()
    s["alcohol"] += 3.0
    s["color_intensity"] += 5.0
    s["proline"] += 800
    return s

for i in range(300):
    data = normal_sample() if i < 150 else drift_sample()
    requests.post(URL, json=data, timeout=3)
    time.sleep(0.3)