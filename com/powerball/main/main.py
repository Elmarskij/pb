# main_script.py
from utility.combinations_generator import CombinationsGenerator


def main():
    """Main execution function to run the process."""

    # Define the input data pools here
    numbers_pool  = [10, 21, 23, 28, 32, 33, 39, 61, 62, 63, 64, 69]
    extras_pool = [4, 18, 21, 24]

    # 1. Initialize the generator with dynamic numbers.
    #    Date calculation runs automatically inside __init__.
    combo_gen = CombinationsGenerator(numbers=numbers_pool, extras=extras_pool)

    # 2. Generate the data
    dataframe = combo_gen.generate_dataframe()

    # 3. Save the data using the orchestration method within the generator
    combo_gen.orchestrate_save(dataframe)


if __name__ == "__main__":
    main()
