from models.registry import get_models
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)
import os, json, pickle
import numpy as np
from evaluation.plot_confusion import plot_confusion_matrices


def train_all_models(X_train,Y_train):
        models = get_models()
        results = {}

        scoring = {
                "accuracy"  : "accuracy",
                "precision" : "precision",
                "recall"    : "recall",
                "f1"        : "f1",
                "roc_auc"   : "roc_auc"
                }

        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        
        for name, model in models.items():
                print(f"Training: {name}")

                cv_scores = cross_validate(
                        model, X_train, Y_train,
                        cv=cv,
                        scoring=scoring,
                        return_train_score=True
                )

                model.fit(X_train,Y_train)

                results[name] = {
                        "model" : model,
                        "val_acc" : cv_scores["test_accuracy"].mean(),
                        "val_pre" : cv_scores["test_precision"].mean(),
                        "val_rec" : cv_scores["test_recall"].mean(),
                        "val_f1" : cv_scores["test_f1"].mean(),
                        "val_auc" : cv_scores["test_roc_auc"].mean(),
                        "train_acc" : cv_scores["train_accuracy"].mean(),
                        "val_acc_std" : cv_scores["test_accuracy"].std(),
                }

                print(f"  val_acc={results[name]['val_acc']:.3f} "
                f"val_f1={results[name]['val_f1']:.3f} "
                f"val_auc={results[name]['val_auc']:.3f}")


        return results

def evaluate_all_models(results, X_test, Y_test):

    print("\n===== Test Set Evaluation =====")

    for name, r in results.items():
        model  = r["model"]

        Y_pred = model.predict(X_test)
        Y_prob = model.predict_proba(X_test)[:, 1]

        r["test_acc"] = accuracy_score(Y_test, Y_pred)
        r["test_pre"] = precision_score(Y_test, Y_pred)
        r["test_rec"] = recall_score(Y_test, Y_pred)
        r["test_f1"]  = f1_score(Y_test, Y_pred)
        r["test_auc"] = roc_auc_score(Y_test, Y_prob)
        r["cm"]       = confusion_matrix(Y_test, Y_pred)
        r["gap"]      = r["train_acc"] - r["val_acc"]

        print(f"\n{name}")
        print(f"  Accuracy  : {r['test_acc']:.4f}")
        print(f"  Precision : {r['test_pre']:.4f}")
        print(f"  Recall    : {r['test_rec']:.4f}")
        print(f"  F1 Score  : {r['test_f1']:.4f}")
        print(f"  ROC-AUC   : {r['test_auc']:.4f}")
        print(f"  Overfit gap: {r['gap']:.4f}",
              "⚠ overfit" if r["gap"] > 0.10 else "✓ healthy")

    return results


def save_best_model(results,
                    model_dir="models",
                    metrics_dir="evaluation"):

    # picking best model by validation AUC
    # (val not test — never use test to make decisions)
    best_name = max(
        results,
        key=lambda n: results[n]["val_auc"]
    )
    best = results[best_name]

    print(f"\n===== Best Model: {best_name} =====")
    print(f"  Val  AUC : {best['val_auc']:.4f}")
    print(f"  Test AUC : {best['test_auc']:.4f}")
    print(f"  Test F1  : {best['test_f1']:.4f}")

  
    os.makedirs(model_dir, exist_ok=True)
    pkl_path = f"{model_dir}/best_model.pkl"
    with open(pkl_path, "wb") as f:
        pickle.dump(best["model"], f)
    print(f"  Saved → {pkl_path}")

   
    os.makedirs(metrics_dir, exist_ok=True)

    metrics_to_save = {}
    for name, r in results.items():
        metrics_to_save[name] = {
            "val_accuracy"  : round(r["val_acc"], 4),
            "val_precision" : round(r["val_pre"], 4),
            "val_recall"    : round(r["val_rec"], 4),
            "val_f1"        : round(r["val_f1"],  4),
            "val_roc_auc"   : round(r["val_auc"], 4),
            "test_accuracy" : round(r["test_acc"],4),
            "test_precision": round(r["test_pre"],4),
            "test_recall"   : round(r["test_rec"],4),
            "test_f1"       : round(r["test_f1"], 4),
            "test_roc_auc"  : round(r["test_auc"],4),
            "overfit_gap"   : round(r["gap"],     4),
            "is_best"       : name == best_name
        }

    json_path = f"{metrics_dir}/metrics.json"
    with open(json_path, "w") as f:
        json.dump(metrics_to_save, f, indent=2)
    print(f"  Saved → {json_path}")

    return best_name, best["model"]

def run_training_pipeline(X_train, X_test, Y_train, Y_test):
 
    print("\n==============================")
    print("   TRAINING PIPELINE START")
    print("==============================")
 
    # step 1 — train + cross-validate
    results = train_all_models(X_train, Y_train)
 
    # step 2 — test set evaluation
    # also stores r["cm"] for each model — plot needs this
    results = evaluate_all_models(results, X_test, Y_test)
 
    # step 3 — pick best, save pkl + json
    best_name, best_model = save_best_model(
        results,
        model_dir="models",
        metrics_dir="evaluation"
    )
 
    # step 4 — confusion matrix plot
    # reads r["cm"] that was stored in step 2
    plot_confusion_matrices(
        results,
        save_dir="evaluation"
    )
 
    print("\n==============================")
    print(f"  DONE. Best model: {best_name}")
    print("  models/best_model.pkl")
    print("  evaluation/metrics.json")
    print("  evaluation/confusion_matrix.png")
    print("==============================")
 
    return best_name, best_model, results