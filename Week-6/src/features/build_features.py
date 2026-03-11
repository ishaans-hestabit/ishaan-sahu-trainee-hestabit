import pandas as pd

def generate_features(df):

    print("------- Generating New Features -------")

    df = df.copy()

    df["FamilySize"] = df["SibSp"] + df["Parch"] + 1

    df["IsAlone"] = (df["FamilySize"] == 1).astype(int)

    df["FarePerPerson"] = df["Fare"] / df["FamilySize"]

    df["AgePclass"] = df["Age"] * df["Pclass"]

    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[0, 12, 18, 35, 60, 100],
        labels=["Child", "Teen", "YoungAdult", "Adult", "Senior"]
    )

    df["FareCategory"] = pd.qcut(
        df["Fare"],
        q=4,
        labels=["Low", "Medium", "High", "VeryHigh"]
    )

    df["Title"] = df["Name"].str.extract(r" ([A-Za-z]+)\.", expand=False)

    df["Deck"] = df["Cabin"].str[0]

    df["TicketLength"] = df["Ticket"].apply(len)

    df["NameLength"] = df["Name"].apply(len)

    print("------- Feature Generation Completed -------")

    df = df.drop(columns=["Name", "Ticket", "Cabin"])

    return df