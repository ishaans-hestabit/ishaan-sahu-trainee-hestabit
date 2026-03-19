import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from features.build_features import generate_features
from features.feature_selector import feature_selection
import os

def encode_features(df):
    print("------- Encoding Features -------")

    df = df.copy()
    categorical_cols = df.select_dtypes(include=["object", "string", "category"]).columns

    df = pd.get_dummies(
        df,
        columns=categorical_cols,
        drop_first=True
    )

    print("------- Encoding Completed -------")
    return df


def normalize_features(X_train, X_test):
    print("------- Normalizing Features -------")

    # only normalize continuous columns — not binary encoded ones
    continuous_cols = [col for col in X_train.columns 
                       if X_train[col].nunique() > 2]

    scaler = StandardScaler()
    
    X_train[continuous_cols] = scaler.fit_transform(X_train[continuous_cols])
    X_test[continuous_cols]  = scaler.transform(X_test[continuous_cols])

    
    print("------- Normalization Completed -------")

    return X_train, X_test


def run_feature_engineering_pipeline():
    df = pd.read_csv("data/processed/final.csv")

    df = generate_features(df)

    # Target is placement status
    X = df.drop("status", axis=1)
    Y = df["status"].map({"Placed": 1, "Not Placed": 0})

    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=42, stratify=Y
    )

    X_train = encode_features(X_train)
    X_test = encode_features(X_test)

    X_train, X_test = X_train.align(X_test, join="left", axis=1, fill_value=0)

    feature_names = X_train.columns

    # X_train, X_test = normalize_features(X_train, X_test)

    X_train, X_test, selected_features = feature_selection(X_train, Y_train, X_test, feature_names)

    print(X_train)

    os.makedirs("data/splits", exist_ok=True)

    # X_train and X_test come out of feature_selection as
    # numpy arrays — wraping them back in DataFrame first
    pd.DataFrame(X_train, columns=selected_features).to_csv("data/splits/X_train.csv", index=False)
    pd.DataFrame(X_test,  columns=selected_features).to_csv("data/splits/X_test.csv",  index=False)
    Y_train.to_csv("data/splits/Y_train.csv", index=False)
    Y_test.to_csv("data/splits/Y_test.csv",   index=False)

    print(f"\n------- Pipeline Complete -------")
    print(f"X_train shape: {X_train.shape}")
    print(f"X_test shape:  {X_test.shape}")
    print(f"Y_train distribution:\n{pd.Series(Y_train).value_counts()}")
    print(f"Y_test distribution:\n{pd.Series(Y_test).value_counts()}")
    print(f"Selected features: {selected_features}")

    return X_train, X_test, Y_train, Y_test
    


run_feature_engineering_pipeline()