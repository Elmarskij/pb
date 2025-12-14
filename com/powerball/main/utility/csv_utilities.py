# csv_utilities.py
import pandas as pd
import os
from pathlib import Path


class CSVUtilities:
    """
    Handles file path construction and saving a DataFrame to a CSV file.
    """

    @staticmethod
    def save_csv(df: pd.DataFrame, formatted_date: str) -> None:
        """Determines the path, ensures directory exists, and saves the CSV."""

        # We determine the base path relative to this utility file's location
        script_dir = Path(__file__).resolve().parent

        # Navigate up from 'utility' to 'powerball', then into 'resources'
        resource_base_dir = script_dir.parent.parent / 'resources'

        target_dir = resource_base_dir / formatted_date

        # Create directories if they don't exist
        os.makedirs(target_dir, exist_ok=True)

        csv_filename_6 = target_dir / f"{formatted_date}.csv"

        df.to_csv(csv_filename_6, index=False)
        print(f"File successfully saved to: {csv_filename_6}")
