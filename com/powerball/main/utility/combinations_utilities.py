import itertools
import logging
from datetime import date

import pandas as pd
from pandas import DataFrame

from .date_utilities import DateUtilities
from .csv_utilities import CSVUtilities


class CombinationsUtilities:
    """
    Generates lottery number combinations and coordinates saving them to a CSV file.
    """

    def __init__(self, numbers: list[int], extras: list[int], filter_map: dict = None) -> None:
        self.numbers: list[int] = numbers
        self.extras: list[int] = extras

        # Optimize: Convert filter lists to SETS for O(1) lookup speed
        self.filter_map = {}
        if filter_map:
            for pos, valid_nums in filter_map.items():
                self.filter_map[pos] = set(valid_nums)

        self.target_date_obj = None
        self.formatted_date = None

        # Call the date calculation logic internally during initialization
        self._set_target_date()
        print(f"CombinationsGenerator initialized for Target Date: {self.formatted_date}")

    def _set_target_date(self) -> None:
        """Uses the helper class to determine and format the target date."""
        date_utils = DateUtilities()
        self.target_date_obj: date = date_utils.get_target_date()
        self.formatted_date: str = self.target_date_obj.strftime("%m-%d-%Y")

    def generate_dataframe(self) -> DataFrame:
        """Generates the DataFrame with Sum, Odd/Even, and Positional Filters."""
        combos_5 = list(itertools.combinations(self.numbers, 5))
        combos_6 = []

        # --- Track used numbers ---
        valid_pool = set()

        logging.info(f"Starting processing of {len(combos_5)} raw combinations...")

        for combo in combos_5:
            # --- 1. POSITIONAL FILTER (NEW) ---
            # combo is (n1, n2, n3, n4, n5). Indices are 0-4.
            # User filter keys are 1-5.
            if self.filter_map:
                # Check if every number is valid for its specific position
                # combo[0] must be in filter_map[1], combo[1] in filter_map[2], etc.
                is_position_valid = True
                for i, number in enumerate(combo):
                    pos_key = i + 1  # Convert 0-index to 1-based key
                    if pos_key in self.filter_map:
                        if number not in self.filter_map[pos_key]:
                            is_position_valid = False
                            break
                if not is_position_valid:
                    continue  # Skip this combination

            # --- 2. SUM CHECK ---
            combo_sum = sum(combo)
            if not (140 <= combo_sum <= 220):
                continue

            # --- 3. ODD/EVEN RATIO CHECK ---
            even_count = sum(1 for n in combo if n % 2 == 0)
            if even_count not in [2, 3]:
                continue

            # --- VALID COMBO FOUND ---
            # Add these numbers to our used pool
            valid_pool.update(combo)

            # --- ADD VALID COMBOS ---
            for extra in self.extras:
                row = list(combo) + [extra]
                combos_6.append(row)

            # Logging every single combo might be too verbose if you have millions.
            # logging.info(f"Valid combo found: {combo}")

        # --- LOG EXECUTION SUMMARY ---
        logging.info("========================================")
        logging.info("       EXECUTION SUMMARY")
        logging.info("========================================")
        logging.info(f"Pool of Main Numbers used in Valid Combos: {sorted(list(valid_pool))}")
        logging.info("----------------------------------------")
        logging.info(f"Total Unique Numbers Used: {len(valid_pool)}")
        logging.info(f"Total Combinations Generated: {len(combos_6)}")
        logging.info("========================================")

        df_6: DataFrame = pd.DataFrame(combos_6, columns=['Num1', 'Num2', 'Num3', 'Num4', 'Num5', 'Num6'])
        return df_6

    def orchestrate_save(self, df) -> None:
        """Passes the DataFrame and date info to the CSV utility class for saving."""
        # Use the utility class's static method
        CSVUtilities.save_csv(df, self.formatted_date)
