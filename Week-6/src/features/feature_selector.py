from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
import json

def feature_selection(X_train,Y_train,X_test, feature_names):
    print("------- Selecting Best Features -------")

    selector = SelectKBest(score_func=f_classif,k = 20)

    X_train_selected = selector.fit_transform(X_train,Y_train)

    X_test_selected = selector.transform(X_test)

    feature_names = feature_names[selector.get_support()].tolist()

    with open("features/feature_list.json", "w") as f:
        json.dump({"selected_features": feature_names}, f, indent=4)

    print("------- Feature Selection Completed -------")

    return X_train_selected, X_test_selected