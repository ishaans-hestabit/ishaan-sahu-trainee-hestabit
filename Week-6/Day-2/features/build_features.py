import pandas as pd
import numpy as np

def generate_features(df):

    print("------- Generating New Features -------")
    df = df.copy()

    df["academic_avg"] = (df["ssc_p"] + df["hsc_p"] + df["degree_p"] + df["mba_p"]) / 4

    df["academic_trend"] = df["mba_p"] - df["ssc_p"]

    df["degree_to_mba_gap"] = df["mba_p"] - df["degree_p"]

    df["etest_vs_mba"] = df["etest_p"] - df["mba_p"]

    df["weighted_academic"] = (
        0.15 * df["ssc_p"] +
        0.20 * df["hsc_p"] +
        0.25 * df["degree_p"] +
        0.20 * df["mba_p"] +
        0.20 * df["etest_p"]
    )

    df["same_board"] = (df["ssc_b"] == df["hsc_b"]).astype(int)

    df["mba_grade"] = pd.cut(
        df["mba_p"],
        bins=[0, 55, 60, 65, 70, 100],
        labels=["Poor", "Average", "Good", "VeryGood", "Excellent"]
    )

    # df["etest_tier"] = pd.qcut(
    #     df["etest_p"],
    #     q=3,
    #     labels=["Low", "Medium", "High"]
    # )

    df["etest_tier"] = pd.cut(df["etest_p"],
                           bins=[0, 64.5, 75.0, 100],
                           labels=["Low","Medium","High"])

    df["is_top_performer"] = (
        (df["ssc_p"] >= 70) &
        (df["hsc_p"] >= 70) &
        (df["degree_p"] >= 70) &
        (df["mba_p"] >= 70)
    ).astype(int)


    print(f"New features added: {10}")
    print("------- Feature Generation Completed -------")

    return df