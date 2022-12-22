import json
import os


if __name__ == "__main__":
    files = os.listdir("../data")
    files = [f for f in files if f.endswith(".json")]
    files = [os.path.join("../data", f) for f in files]
    data = []
    for f in files:
        with open(f, "r") as f:
            data.extend(json.load(f))
    with open("../data/nominatim_detailed_result.json", "w") as f:
        json.dump(data, f, indent=2)