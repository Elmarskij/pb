# main_script.py
from com.powerball.main.app.combinations_generator import CombinationsGenerator


def main():
    """Main execution function to run the process."""

    # Define the input data pools here
    numbers_pool  = [10, 21, 23, 28, 32, 33, 39, 61, 62, 63, 64, 69]
    extras_pool = [4, 18, 21, 24]

    # Initialize and run the generator
    CombinationsGenerator.generate_combinations(numbers_pool, extras_pool)


if __name__ == "__main__":
    main()
