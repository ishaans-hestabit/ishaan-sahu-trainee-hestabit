import numpy as np
import matplotlib.pyplot as plt
import os

def plot_feature_importance(model, X_test, Y_test, feature_names, model_name, save_dir="evaluation"):
   
    importances = getattr(model, "feature_importances_", None)
    if importances is None: 
        importances = np.abs(model.coef_[0])

   
    idx = np.argsort(importances)[-15:]
    names, scores = np.array(feature_names)[idx], importances[idx]

   
    fig, ax = plt.subplots(figsize=(10, 7))
    bars = ax.barh(names, scores, color="#378ADD", alpha=0.8)
    
    
    ax.bar_label(bars, fmt='%.3f', padding=3, fontsize=9, color="gray")

    ax.set_title(f"Feature Importance — {model_name}", fontsize=13)
    plt.tight_layout()

  
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(f"{save_dir}/importance_{model_name.replace(' ', '_')}.png", bbox_inches="tight", dpi=150)
    plt.close()