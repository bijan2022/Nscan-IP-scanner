import json
import os

def save_results(results, filepath="results/scan_results.json"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"Results saved to {filepath}")