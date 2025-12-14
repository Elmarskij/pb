# combinations_generator.py
import itertools
from datetime import date

import pandas as pd
from pandas import DataFrame

# Import the helper classes
from .date_utilities import LotteryDateCalculator
from .csv_utilities import CSVUtilities


class CombinationsGenerator:
    """
    Generates lottery number combinations and coordinates saving them to a CSV file.
    """

    def __init__(self, numbers: list, extras: list) -> None:
        self.numbers: list[int] = numbers
        self.extras: list[int] = extras
        self.target_date_obj = None
        self.formatted_date = None

        # Call the date calculation logic internally during initialization
        self._set_target_date()
        print(f"CombinationsGenerator initialized for Target Date: {self.formatted_date}")

    def _set_target_date(self) -> None:
        """Uses the helper class to determine and format the target date."""
        date_calc = LotteryDateCalculator()
        self.target_date_obj: date = date_calc.get_target_date()
        self.formatted_date: str = self.target_date_obj.strftime("%m-%d-%Y")

    def generate_dataframe(self) -> DataFrame:
        """Generates the pandas DataFrame of combinations."""
        # ... (combination generation logic remains the same) ...
        combos_5 = list(itertools.combinations(self.numbers, 5))
        combos_6 = []
        for combo in combos_5:
            for extra in self.extras:
                row = list(combo) + [extra]
                combos_6.append(row)
        df_6: DataFrame = pd.DataFrame(combos_6, columns=['Num1', 'Num2', 'Num3', 'Num4', 'Num5', 'Num6'])
        return df_6

    def orchestrate_save(self, df) -> None:
        """Passes the DataFrame and date info to the CSV utility class for saving."""
        # Use the utility class's static method
        CSVUtilities.save_csv(df, self.formatted_date)
