import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from features.build_features import generate_features
from features.feature_selector import feature_selection


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


def normalize_features(X_train,X_test):
    print("------- Normalizing Features -------")

    scaler = StandardScaler()

    X_train_normalised = scaler.fit_transform(X_train)
    X_test_normalised = scaler.transform(X_test)

    print("------- Normalization Completed -------")

    return X_train_normalised,X_test_normalised



def run_feature_engineering_pipeline():
    df = pd.read_csv("data/processed/final.csv")
    df = generate_features(df)

    X = df.drop("Survived", axis=1)
    Y = df["Survived"]

    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=42
    )

    X_train = encode_features(X_train)
    X_test = encode_features(X_test)

    X_train, X_test = X_train.align(X_test, join="left", axis=1, fill_value=0)

    feature_names = X_train.columns

    X_train , X_test = normalize_features(X_train, X_test)

    X_train, X_test = feature_selection(X_train,Y_train,X_test, feature_names)


    print(X_train)

run_feature_engineering_pipeline()