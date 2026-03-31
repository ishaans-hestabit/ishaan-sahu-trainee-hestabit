import seaborn as sns
import matplotlib.pyplot as plt
import os
import pandas as pd

def plot_error_analysis(model, X_test, Y_test, feature_names, model_name, save_dir="evaluation"):
    
    Y_pred = model.predict(X_test)
    X_df = pd.DataFrame(X_test, columns=feature_names)
    Y_test = pd.Series(Y_test).values
    
    masks = {
        "True Placed": (Y_pred == 1) & (Y_test == 1),
        "Missed Placed": (Y_pred == 0) & (Y_test == 1),
        "False Alarm": (Y_pred == 1) & (Y_test == 0),
        "True Not Placed": (Y_pred == 0) & (Y_test == 0)
    }

    
    data = pd.DataFrame({k: X_df[v][feature_names[:10]].mean() for k, v in masks.items() if v.any()})

    norm_data = data.apply(lambda x: (x - x.min()) / (x.max() - x.min() + 1e-8), axis=1)

    
    plt.figure(figsize=(12, 8))
    sns.heatmap(norm_data, annot=True, fmt=".2f", cmap="RdYlGn", cbar_kws={'label': 'Normalized Mean'})
    
    plt.title(f"Error Analysis — {model_name}")
    plt.tight_layout()
    
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(f"{save_dir}/error_{model_name}.png", dpi=150)
    plt.close()