import os
import matplotlib.pyplot as plt

def plot_confusion_matrices(results, save_dir="evaluation"):

    n = len(results)  

    fig, axes = plt.subplots(
        1, n,
        figsize=(5 * n, 4)  
    )

    for ax, (name, r) in zip(axes, results.items()):
        cm = r["cm"] 

        ax.imshow(cm, cmap="Blues")

        
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(["Not Placed", "Placed"], fontsize=9)
        ax.set_yticklabels(["Not Placed", "Placed"], fontsize=9)
        ax.set_xlabel("Predicted", fontsize=10)
        ax.set_ylabel("Actual",    fontsize=10)

        
        ax.set_title(
            f"{name}\n"
            f"acc={r['test_acc']:.2f}  "
            f"f1={r['test_f1']:.2f}  "
            f"rec={r['test_rec']:.2f}",
            fontsize=10
        )

    
        for i in range(2):
            for j in range(2):
                color = "white" if cm[i, j] > cm.max() / 2 else "black"
                ax.text(
                    j, i,
                    str(cm[i, j]),
                    ha="center", va="center",
                    fontsize=16, fontweight="bold",
                    color=color
                )

    plt.suptitle(
        "Confusion Matrices — All Models",
        fontsize=13, y=1.02
    )
    plt.tight_layout()

    os.makedirs(save_dir, exist_ok=True)
    path = f"{save_dir}/confusion_matrix.png"
    plt.savefig(path, bbox_inches="tight", dpi=150)
    plt.close()

    print(f"  Saved → {path}")