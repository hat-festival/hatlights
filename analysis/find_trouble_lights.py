import yaml
from pathlib import Path

locations = yaml.safe_load(Path("../conf/locations.yaml").read_text())

no_x = []
no_z = []

for index, data in enumerate(locations):
    if "x" not in data:
        no_x.append(index)

    if "z" not in data:
        no_z.append(index)

print(f"No 'x' for {no_x}")
print(f"No 'z' for {no_z}")
