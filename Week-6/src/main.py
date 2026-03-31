from pipelines.feature_engineering_pipeline import run_feature_engineering_pipeline
import json, pickle
from training.train import run_training_pipeline
from training.tune import run_tuning_pipeline
from evaluation.explainability import run_explainability, report_improvement

X_train, X_test, y_train, y_test = run_feature_engineering_pipeline()

with open("features/feature_list.json") as f:
    feature_names = json.load(f)["selected_features"]


baseline_best_name, baseline_best_model, baseline_results = run_training_pipeline( X_train, X_test, y_train, y_test)


tuned_best_name, tuned_results = run_tuning_pipeline(X_train, X_test, y_train, y_test)

baseline_auc = baseline_results[baseline_best_name]["val_auc"]
tuned_auc = tuned_results[tuned_best_name]["val_auc"]


use_tuned = tuned_auc >= baseline_auc

if use_tuned:
    chosen_model = tuned_results[tuned_best_name]["model"]
    chosen_name = f"{tuned_best_name}"
else:
    chosen_model = baseline_results[baseline_best_name]["model"]
    chosen_name = f"{baseline_best_name}"


with open("models/best_model_prod.pkl", "wb") as f:
    pickle.dump(chosen_model, f)


run_explainability(chosen_model, X_test, y_test, feature_names, chosen_name)


report_improvement()