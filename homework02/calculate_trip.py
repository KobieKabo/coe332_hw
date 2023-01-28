# Jakob Long
# Jrl4725

import json
import math

mars_radius = 3389.5    # km

def calc_gcd(latitude_1: float, longitude_1: float, latitude_2: float, longitude_2: float) -> float:
    lat1, lon1, lat2, lon2 = map( math.radians, [latitude_1, longitude_1, latitude_2, longitude_2] )
    d_sigma = math.acos( math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(abs(lon1-lon2)))
    return ( mars_radius * d_sigma )

with open("meteorite_landing_sites.json", "r") as f:
    data = json.load(f)

# Robot speed in km/hr
speed = 10

# Starting coordinates
start_lat, start_lon = 16.0, 82.0

# Total time and distance for the trip
total_time, total_distance = 0, 0

# Iterate over each site
for i, site in enumerate(data["sites"]):
    time = calc_gcd(start_lat, start_lon, site["latitude"], site["longitude"]) / speed
    distance = calc_gcd(start_lat, start_lon, site["latitude"], site["longitude"])
    sample_time = 0
    if site["composition"] == "stony":
        sample_time = 1
    elif site["composition"] == "iron":
        sample_time = 2
    elif site["composition"] == "stony-iron":
        sample_time = 3

    # Update total time and distance
    total_time += time + sample_time
    total_distance += distance
    print(f"Leg {i+1}: Distance = {distance:.2f} km, Travel Time = {time:.2f} hr, Sample Time = {sample_time} hr")
    start_lat, start_lon = site["latitude"], site["longitude"]

# Print summary
print(f"Total Distance = {total_distance:.2f} km, Total Time = {total_time:.2f} hr")     