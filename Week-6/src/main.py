from pipelines.feature_engineering_pipeline import run_feature_engineering_pipeline
import json
from training.train import run_training_pipeline
from training.tune import run_tuning_pipeline
from evaluation.explainability import run_explainability ,report_improvement

X_train, X_test, y_train, y_test = run_feature_engineering_pipeline()



with open("features/feature_list.json") as f:
    feature_names = json.load(f)["selected_features"]


run_training_pipeline(X_train,X_test, y_train, y_test)

best_name, tuned_results = run_tuning_pipeline(X_train, X_test, y_train, y_test)

best_model = tuned_results[best_name]["model"]

run_explainability(best_model, X_test, y_test, feature_names, best_name)

report_improvement()