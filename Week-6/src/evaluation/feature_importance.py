import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.inspection import permutation_importance

def plot_feature_importance(model, X_test, Y_test,
                             feature_names,
                             model_name,
                             save_dir="evaluation"):

    print(f"\nGenerating feature importance for: {model_name}")

    model_type = type(model).__name__

   
    if model_type in ["RandomForestClassifier","XGBClassifier"]:
       
        importances = model.feature_importances_

    elif model_type == "LogisticRegression":
       
        importances = np.abs(model.coef_[0])

    else:
       
        result      = permutation_importance(
                          model, X_test, Y_test,
                          n_repeats=10,
                          random_state=42,
                          scoring="roc_auc"
                      )
        importances = result.importances_mean

   
    indices = np.argsort(importances)[::-1][:15]  # top 15
    top_features    = [feature_names[i] for i in indices]
    top_importances = importances[indices]

    
    fig, ax = plt.subplots(figsize=(10, 7))

    bars = ax.barh(
        range(len(top_features)),
        top_importances[::-1],  
        color="#378ADD",
        alpha=0.8
    )

    ax.set_yticks(range(len(top_features)))
    ax.set_yticklabels(top_features[::-1], fontsize=11)
    ax.set_xlabel("Importance Score", fontsize=11)
    ax.set_title(
        f"Feature Importance — {model_name}",
        fontsize=13
    )

    for bar, val in zip(bars, top_importances[::-1]):
        ax.text(
            bar.get_width() + 0.001,
            bar.get_y() + bar.get_height()/2,
            f"{val:.3f}",
            va="center", fontsize=9,
            color="gray"
        )

    plt.tight_layout()

    os.makedirs(save_dir, exist_ok=True)
    path = f"{save_dir}/feature_importance_{model_name.replace(' ','_')}.png"
    plt.savefig(path, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"  Saved → {path}")