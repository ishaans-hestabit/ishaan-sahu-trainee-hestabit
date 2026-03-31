import matplotlib.pyplot as plt
import os
from sklearn.metrics import ConfusionMatrixDisplay

def plot_confusion_matrices(results, save_dir="evaluation"):
    n = len(results)
    
    fig, axes = plt.subplots(1, n, figsize=(5 * n, 4), squeeze=False)

    for ax, (name, r) in zip(axes.flatten(), results.items()):
        
        disp = ConfusionMatrixDisplay(confusion_matrix=r["cm"], 
                                      display_labels=["Placed (1)", "Not Placed (0)"])
        
        
        disp.plot(ax=ax, cmap="Blues", colorbar=False)
        
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")

    plt.suptitle("Confusion Matrices — All Models", fontsize=13, y=1.05)
    plt.tight_layout()
    
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(f"{save_dir}/confusion_matrix.png", bbox_inches="tight", dpi=150)
    plt.close()