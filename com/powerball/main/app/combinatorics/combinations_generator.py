# main_script.py
from com.powerball.main.utility.combinations_utilities import CombinationsUtilities

class CombinationsGenerator:

    @staticmethod
    def generate_combinations(numbers_pool: list[int], extras_pool: list[int]) -> None:
        """Main execution function to run the process."""

        # 1. Initialize the generator with dynamic numbers.
        #    Date calculation runs automatically inside __init__.
        combo_gen = CombinationsUtilities(numbers=numbers_pool, extras=extras_pool)

        # 2. Generate the data
        dataframe = combo_gen.generate_dataframe()

        # 3. Save the data using the orchestration method within the generator
        combo_gen.orchestrate_save(dataframe)
