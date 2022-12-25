import os
import json


if __name__ == "__main__":
    with open(os.path.join("new_results", "new_all_webcams_with_ip.json"), "r") as f:
        raw_results = json.load(f)
    results = []
    for webcam in raw_results:
        webcam["ip"] = None
        if webcam["ip_from_original_url"] is not None:
            webcam["ip"] = webcam["ip_from_original_url"]
        else:
            webcam["ip"] = webcam["ip_from_secondary_url"]
        if webcam["ip"] is not None:
            results.append(webcam)
    with open(os.path.join("new_results", "all_webcams_with_ip.json"), "w") as f:
        json.dump(results, f)
    print(len(results))
