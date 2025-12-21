from com.powerball.main.utility.combinations_utilities import CombinationsUtilities

class CombinationsGenerator:

    @staticmethod
    def generate_combinations(numbers_pool: list[int], extras_pool: list[int], filter_map: dict = None) -> None:
        """Main execution function to run the process."""

        # 1. Initialize with filters
        combo_gen = CombinationsUtilities(
            numbers=numbers_pool, 
            extras=extras_pool, 
            filter_map=filter_map
        )

        # 2. Generate the data
        dataframe = combo_gen.generate_dataframe()

        # 3. Save the data
        combo_gen.orchestrate_save(dataframe)
