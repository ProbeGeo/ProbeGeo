import os
import json


if __name__ == "__main__":
    all_results = []
    for file in os.listdir("results"):
        if file.startswith("webcams"):
            with open(os.path.join("results", file), "r") as f:
                all_results.extend(json.load(f))
    with open("results/all_webcams.json", "w") as f:
        json.dump(all_results, f)