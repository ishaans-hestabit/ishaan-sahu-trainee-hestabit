import os
import json
import pickle

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)
from xgboost import XGBClassifier

CV = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

def tune_logistic_regression(X_train, Y_train):
    print("\nTuning: Logistic Regression")

    param_grid = {
        "C"      : [0.01, 0.1, 1.0, 10.0, 100.0],
        "penalty": ["l1", "l2"],
        "solver" : ["liblinear"],
    }
    

    grid = GridSearchCV(
        LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced"),
        param_grid,
        cv=CV,
        scoring="roc_auc", 
        n_jobs=-1,       
        verbose=1
    )

    grid.fit(X_train, Y_train)

    print(f"  Best params : {grid.best_params_}")
    print(f"  Best val AUC: {grid.best_score_:.4f}")

    return grid.best_estimator_, grid.best_params_, grid.best_score_


def tune_random_forest(X_train, Y_train):
    print("\nTuning: Random Forest")

    param_grid = {
        "n_estimators"     : [50, 100, 200],
        "max_depth"        : [3, 5, 7, None],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf" : [1, 2, 4],
    }
    

    grid = GridSearchCV(
        RandomForestClassifier(random_state=42, class_weight="balanced"),
        param_grid,
        cv=CV,
        scoring="roc_auc",
        n_jobs=-1,
        verbose=1
    )

    grid.fit(X_train, Y_train)

    print(f"  Best params : {grid.best_params_}")
    print(f"  Best val AUC: {grid.best_score_:.4f}")

    return grid.best_estimator_, grid.best_params_, grid.best_score_


def tune_xgboost(X_train, Y_train):
    print("\nTuning: XGBoost")

    param_grid = {
        "n_estimators"    : [50, 100, 200],
        "max_depth"       : [3, 4, 5],
        "learning_rate"   : [0.01, 0.1, 0.2],
        "subsample"       : [0.8, 1.0],
        "colsample_bytree": [0.8, 1.0],
    }
    #

    grid = GridSearchCV(
        XGBClassifier(
            random_state=42,
            eval_metric="logloss",
            verbosity=0,
        ),
        param_grid,
        cv=CV,
        scoring="roc_auc",
        n_jobs=-1,
        verbose=1
    )

    grid.fit(X_train, Y_train)

    print(f"  Best params : {grid.best_params_}")
    print(f"  Best val AUC: {grid.best_score_:.4f}")

    return grid.best_estimator_, grid.best_params_, grid.best_score_


def tune_neural_network(X_train, Y_train):
    print("\nTuning: Neural Network")

    param_grid = {
        "hidden_layer_sizes": [
            (32,),
            (64,),
            (64, 32),
            (128, 64),
            (64, 32, 16),
        ],
        "alpha"            : [0.0001, 0.001, 0.01],
        "learning_rate_init": [0.001, 0.01],
        "activation"       : ["relu", "tanh"],
    }

    grid = GridSearchCV(
        MLPClassifier(max_iter=500, random_state=42),
        param_grid,
        cv=CV,
        scoring="roc_auc",
        n_jobs=-1,
        verbose=1
    )

    grid.fit(X_train, Y_train)

    print(f"  Best params : {grid.best_params_}")
    print(f"  Best val AUC: {grid.best_score_:.4f}")

    return grid.best_estimator_, grid.best_params_, grid.best_score_



def run_tuning_pipeline(X_train, X_test, Y_train, Y_test):
   

    tuners = {
        "Logistic Regression": tune_logistic_regression,
        "Random Forest"      : tune_random_forest,
        "XGBoost"            : tune_xgboost,
        "Neural Network"     : tune_neural_network,
    }

    tuned_results = {}

    for name, tune_fn in tuners.items():

        best_model, best_params, best_val_auc = tune_fn(X_train, Y_train)

        Y_pred = best_model.predict(X_test)
        Y_prob = best_model.predict_proba(X_test)[:, 1]

        tuned_results[name] = {
            "model"      : best_model,
            "best_params": best_params,
            "val_auc"    : round(best_val_auc,                    4),
            "test_acc"   : round(accuracy_score(Y_test, Y_pred),  4),
            "test_pre"   : round(precision_score(Y_test, Y_pred), 4),
            "test_rec"   : round(recall_score(Y_test, Y_pred),    4),
            "test_f1"    : round(f1_score(Y_test, Y_pred),        4),
            "test_auc"   : round(roc_auc_score(Y_test, Y_prob),   4),
        }

        print(f"\n  {name} test results:")
        print(f"    Accuracy  : {tuned_results[name]['test_acc']}")
        print(f"    Precision : {tuned_results[name]['test_pre']}")
        print(f"    Recall    : {tuned_results[name]['test_rec']}")
        print(f"    F1        : {tuned_results[name]['test_f1']}")
        print(f"    ROC-AUC   : {tuned_results[name]['test_auc']}")

    best_name = max(
        tuned_results,
        key=lambda n: tuned_results[n]["val_auc"]
    )

    print(f"\n===== Best Tuned Model: {best_name} =====")
    print(f"  Best params: {tuned_results[best_name]['best_params']}")
    print(f"  Val  AUC   : {tuned_results[best_name]['val_auc']}")
    print(f"  Test AUC   : {tuned_results[best_name]['test_auc']}")
    print(f"  Test F1    : {tuned_results[best_name]['test_f1']}")

    os.makedirs("models", exist_ok=True)
    with open("models/best_model_tuned.pkl", "wb") as f:
        pickle.dump(tuned_results[best_name]["model"], f)
    print("\nSaved → models/best_model_tuned.pkl")

    # save all tuned metrics
    os.makedirs("evaluation", exist_ok=True)
    metrics = {
        name: {k: v for k, v in r.items() if k != "model"}
        for name, r in tuned_results.items()
    }
    with open("evaluation/tuned_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    print("Saved → evaluation/tuned_metrics.json")

    print("\n==============================")
    print("   TUNING COMPLETE")
    print("==============================")

    return best_name, tuned_results