import pandas as pd
import os

RAW_DATA_PATH = "data/raw/Titanic-Dataset.csv"
PROCESSED_DATA_PATH = "data/processed/final.csv"

def load_data(filepath):
        print(f"------ Loading Data from file at {filepath} ------")

        df = pd.read_csv(filepath)
        
        print("------- File Loaded -------")
        return df

def clean_data(df):
        print(f"------- Cleaning Data -------")
        df = df.copy()

        # if data.duplicated().sum() = 0 i.e. no duplicate rows
        df = df.drop_duplicates() # removed duplicates if any


        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'str']).columns.tolist()

        for col in numeric_cols:
            null_count = df[col].isnull().sum()
            if null_count == 0:
                continue
            fill_val = df[col].median()
            df[col] = df[col].fillna(fill_val)

        for col in categorical_cols:
            null_count = df[col].isnull().sum()
            if null_count == 0:
                 continue
            fill_val = "Unknown"
            df[col] = df[col].fillna(fill_val)


        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            df[col] = df[col].clip(lower=Q1 - 1.5 * IQR, upper=Q3 + 1.5 * IQR)

        print("------- Data Cleaned -------")
        return df

def save_processed_data(df, output_path):
    print("------- Saving Data -------")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path,index=False)

    print("------- Data Saved -------")


def run_pipeline(input_path, output_path):
        
        raw_df = load_data(input_path)

        cleaned_df = clean_data(raw_df)

        save_processed_data(cleaned_df,output_path)

        return cleaned_df


run_pipeline(RAW_DATA_PATH, PROCESSED_DATA_PATH)