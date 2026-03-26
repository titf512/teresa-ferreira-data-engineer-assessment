"""Module responsible for transforming csv files."""
import pandas as pd


class Transformer:
    """Handles all business logic and data enrichments."""
    def __init__(self, csv_path):
        """Initializes the Transformer with the csv path."""
        self.csv_path = csv_path
        self.df = pd.read_csv(self.csv_path)

    def add_a_count_column(self):
        """Add the 'a_count' column to the csv file."""
        #Using Pandas for simplicity and standard data manipulation.

        column_name = "FinInstrmGnlAttrbts.FullNm"
        self.df['a_count'] = self.df[column_name].astype(str).str.count('a')

        self.df.to_csv(self.csv_path, index=False)


    def add_contains_a_column(self):
        """Adds the 'acontains_a' column to the csv file."""
        # Logic: "YES" if a_count > 0, "NO" otherwise.
        self.df['contains_a'] = self.df['a_count'].apply(lambda x: "YES" if x > 0 else "NO")
        self.df.to_csv(self.csv_path, index=False)