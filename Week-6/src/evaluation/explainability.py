import json
from evaluation.shap_analysis import plot_shap_summary
from evaluation.feature_importance import plot_feature_importance
from evaluation.error_analysis import plot_error_analysis


def run_explainability(best_model, X_test, Y_test, feature_names, model_name, save_dir="evaluation"):
    print("\n===== EXPLAINABILITY =====")

    plot_shap_summary(best_model, X_test, feature_names, model_name, save_dir)

    plot_feature_importance(best_model, X_test, Y_test, feature_names, model_name, save_dir)
    
    plot_error_analysis(best_model, X_test, Y_test, feature_names, model_name, save_dir)

    print("All explainability plots saved.")


def report_improvement(baseline_json="evaluation/metrics.json", tuned_json="evaluation/tuned_metrics.json"):
    print("\n===== Improvement Over Baseline =====")

    baseline = json.load(open(baseline_json))
    tuned = json.load(open(tuned_json))

    for name in baseline:
        if name not in tuned:
            continue

        b_auc = baseline[name]["test_roc_auc"]
        t_auc = tuned[name]["test_auc"]
        b_f1 = baseline[name]["test_f1"]
        t_f1 = tuned[name]["test_f1"]

        print(f"\n{name}")
        print(f"  AUC : {b_auc} -> {t_auc}  ({'↑' if t_auc > b_auc else '↓'}{abs(round(t_auc - b_auc, 4))})")
        print(f"  F1  : {b_f1} -> {t_f1}  ({'↑' if t_f1 > b_f1 else '↓'}{abs(round(t_f1 - b_f1, 4))})")