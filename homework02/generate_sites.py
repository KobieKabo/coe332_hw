# Jakob Long
# Jrl4725

import json
import random

latitude = [random.uniform(16.0, 18.0) for _ in range(5)]
longitude = [random.uniform(82.0, 84.0) for _ in range(5)]
composition = [random.choice(["stony", "iron", "stony-iron"]) for _ in range(5)]

data = {"sites": [{"latitude": lat, "longitude": lon, "composition": comp} 
                  for lat, lon, comp in zip(latitude, longitude, composition)]}

with open("meteorite_landing_sites.json", "w") as f:
    json.dump(data, f, indent = 2)