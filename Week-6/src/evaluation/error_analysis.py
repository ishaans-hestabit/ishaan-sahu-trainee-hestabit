import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_error_analysis(model, X_test, Y_test,
                         feature_names,
                         model_name,
                         save_dir="evaluation"):

    print(f"\nGenerating error analysis for: {model_name}")

    Y_pred = model.predict(X_test)
    X_df   = pd.DataFrame(X_test, columns=feature_names)
    Y_test = np.array(Y_test)

   
    tp_mask = (Y_pred == 1) & (Y_test == 1) 
    fn_mask = (Y_pred == 0) & (Y_test == 1) 
    fp_mask = (Y_pred == 1) & (Y_test == 0)  
    tn_mask = (Y_pred == 0) & (Y_test == 0)  

    groups = {
        f"True Placed\n(n={tp_mask.sum()})"      : X_df[tp_mask],
        f"Missed Placed\n(n={fn_mask.sum()})"    : X_df[fn_mask],
        f"False Alarm\n(n={fp_mask.sum()})"      : X_df[fp_mask],
        f"True Not Placed\n(n={tn_mask.sum()})"  : X_df[tn_mask],
    }

   
    top_features = feature_names[:10]

    heatmap_data = pd.DataFrame({
        label: group[top_features].mean()
        for label, group in groups.items()
        if len(group) > 0          
    })

   
    heatmap_norm = heatmap_data.apply(
        lambda row: (row - row.min()) /
                    (row.max() - row.min() + 1e-8),
        axis=1
    )

    
    fig, ax = plt.subplots(
        figsize=(len(heatmap_norm.columns) * 2.5, 8)
    )

    im = ax.imshow(
        heatmap_norm.values,
        cmap="RdYlGn",    
        aspect="auto",
        vmin=0, vmax=1
    )

    ax.set_xticks(range(len(heatmap_norm.columns)))
    ax.set_xticklabels(heatmap_norm.columns,
                        fontsize=10, rotation=15)
    ax.set_yticks(range(len(top_features)))
    ax.set_yticklabels(top_features, fontsize=10)

    # add normalized value in each cell
    for i in range(len(top_features)):
        for j in range(len(heatmap_norm.columns)):
            val = heatmap_norm.values[i, j]
            ax.text(j, i, f"{val:.2f}",
                    ha="center", va="center",
                    fontsize=9,
                    color="black" if 0.3 < val < 0.7
                          else "white")

    plt.colorbar(im, ax=ax, label="Normalized mean value")
    ax.set_title(
        f"Error Analysis Heatmap — {model_name}\n"
        f"Comparing feature profiles across prediction groups",
        fontsize=12
    )
    plt.tight_layout()

    os.makedirs(save_dir, exist_ok=True)
    path = f"{save_dir}/error_analysis_{model_name.replace(' ','_')}.png"
    plt.savefig(path, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"  Saved → {path}")