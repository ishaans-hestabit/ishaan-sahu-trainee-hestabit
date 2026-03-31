import shap
import pandas as pd
import matplotlib.pyplot as plt
import os


def plot_shap_summary(model, X_test, feature_names, model_name, save_dir="evaluation"):
    print(f"\nSHAP plot: {model_name}")

    model_type = type(model).__name__

    if model_type in ["RandomForestClassifier", "XGBClassifier"]:

        explainer = shap.TreeExplainer(model)

        shap_values = explainer.shap_values(X_test)

        if isinstance(shap_values, list):
            shap_values = shap_values[1]


    elif model_type == "LogisticRegression":

        explainer = shap.LinearExplainer(model, X_test, feature_perturbation="interventional")

        shap_values = explainer.shap_values(X_test)

    else:

        background = shap.kmeans(X_test, 10)

        explainer = shap.KernelExplainer(model.predict_proba, background)

        shap_values = explainer.shap_values(X_test[:50], nsamples=100)

        if isinstance(shap_values, list):
            shap_values = shap_values[1]
            
        X_test = X_test[:50]

    X_df = pd.DataFrame(X_test, columns=feature_names)

    plt.figure(figsize=(10, 8))
    shap.summary_plot(shap_values, X_df, show=False, max_display=15, plot_type="dot")
    plt.title(f"SHAP Summary — {model_name}", fontsize=13)
    plt.tight_layout()

    os.makedirs(save_dir, exist_ok=True)
    path = f"{save_dir}/shap_summary_{model_name.replace(' ', '_')}.png"
    plt.savefig(path, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"Saved -> {path}")