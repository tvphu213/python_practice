from scripts.python.get_conf import Config
import pandas as pd
from scripts.python.preprocess_data import PreProcessData


def main():
    df = pd.read_csv('data/input/sample_data.csv')
    columns = list(df.columns)
    process_obj = PreProcessData(df)
    for column in columns:
        process_obj.validate_email(column)
        process_obj.numeric_validate(column)
        process_obj.datetime_validate(column)


if __name__ == "__main__":
    main()
