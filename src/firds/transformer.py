"""Module responsible for transforming csv files."""
import pandas as pd


class Transformer:
    """Handles all business logic and data enrichments."""
    def __init__(self, csv_path):
        """Initializes the Transformer with the csv path."""
        self.csv_path = csv_path

    def add_a_count_column(self):
        """Add the 'a_count' column to the csv file."""
        #Using Pandas for simplicity and standard data manipulation.
        df = pd.read_csv(self.csv_path)

        column_name = "FinInstrmGnlAttrbts.FullNm"
        df['a_count'] = df[column_name].astype(str).str.count('a')

        df.to_csv(self.csv_path, index=False)