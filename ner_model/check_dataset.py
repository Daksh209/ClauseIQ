import json

with open("CUAD_v1/CUAD_v1.json") as f:
    data = json.load(f)

print(type(data))
print(len(data["data"]))
print(data["data"][0].keys())