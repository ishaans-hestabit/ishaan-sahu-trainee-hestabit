from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.preprocessing import StandardScaler
import json
import pickle

def feature_selection(X_train, Y_train, X_test, feature_names):
    print("------- Selecting Best Features -------")

    k = min(20, X_train.shape[1])
    selector = SelectKBest(score_func=mutual_info_classif, k=k)

    X_train_selected = selector.fit_transform(X_train, Y_train)
    X_test_selected  = selector.transform(X_test)

    selected_features = feature_names[selector.get_support()].tolist()

    # fit scaler on the 20 selected features directly
    scaler = StandardScaler()
    X_train_selected = scaler.fit_transform(X_train_selected)
    X_test_selected  = scaler.transform(X_test_selected)

    with open("features/feature_list.json", "w") as f:
        json.dump({"selected_features": selected_features}, f, indent=4)

    with open("models/selector.pkl", "wb") as f:
        pickle.dump(selector, f)

    with open("models/scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    print(f"Selected {k} features from {len(feature_names)} total")
    print("------- Feature Selection Completed -------")

    return X_train_selected, X_test_selected, selected_features