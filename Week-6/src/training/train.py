def save_best_model(results,
                    model_dir="models",
                    metrics_dir="evaluation"):

    # combined score — rewards high AUC, penalises overfitting beyond 0.10
    def combined_score(name):
        auc = results[name]["val_auc"]
        gap = results[name]["gap"]
        penalty = max(0, gap - 0.10)
        return auc - penalty

    # ← only this block changed, everything below is identical
    best_name = max(results, key=combined_score)

    # print so you can see why it chose what it chose
    print("\n===== Model Selection Scores =====")
    for name in results:
        r = results[name]
        penalty = max(0, r["gap"] - 0.10)
        score   = r["val_auc"] - penalty
        print(f"  {name}: val_auc={r['val_auc']:.4f}  gap={r['gap']:.4f}  score={score:.4f}")

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