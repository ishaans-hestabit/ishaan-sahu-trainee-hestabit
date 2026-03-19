from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier 
from sklearn.neural_network import MLPClassifier

def get_models():
    return {
        "Logistic Regression": LogisticRegression(
            C=1.0, penalty="l2",
            solver="lbfgs", max_iter=1000,
            random_state=42,
            class_weight="balanced"
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, max_depth=5,
            random_state=42,
            class_weight="balanced"
        ),
        "XGBoost": XGBClassifier(
            n_estimators=100, max_depth=4,
            random_state=42, learning_rate=0.1,
            eval_metric="logloss",
            scale_pos_weight=148/67       # ← XGBoost equivalent of class_weight
        ),
        "Neural Network":MLPClassifier(
            hidden_layer_sizes=(64,32),
            max_iter=500, random_state=42
        )
    }