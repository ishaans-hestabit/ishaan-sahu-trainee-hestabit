import pandas as pd
import json

def check_drift(logs_path="prediction_logs.csv",
                reference_path="data/processed/final.csv",
                threshold=0.2):

    with open("features/feature_list.json") as f:
        features = json.load(f)["selected_features"]

    # use only features that exist in final.csv (non-encoded ones)
    raw_features = ['ssc_p', 'hsc_p', 'degree_p', 'etest_p']

    reference = pd.read_csv(reference_path)[raw_features]
    logs      = pd.read_csv(logs_path)

    if len(logs) == 0:
        print("No predictions logged yet")
        return

    print(f"Checking drift across {len(raw_features)} features...\n")

    for col in raw_features:
        ref  = reference[col].mean()
        curr = logs[col].mean()
        change = abs(curr - ref) / abs(ref) if ref != 0 else abs(curr)

        status = "⚠ DRIFT" if change > threshold else "✓ ok"
        print(f"{status} | {col} | train={ref:.2f} now={curr:.2f} change={change*100:.1f}%")


if __name__ == "__main__":
    check_drift()