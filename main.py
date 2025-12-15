# main_script.py
import logging
import re

from com.powerball.main.app.combinations_generator import CombinationsGenerator
from com.powerball.main.rest.lotto_net import LottoNetAPI

# To enable logging for all levels, set the level to DEBUG and define the format.
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)


def generate_combinations():
    """Main execution function to run the process."""

    # Define the input data pools here
    numbers_pool = [10, 21, 23, 28, 32, 33, 39, 61, 62, 63, 64, 69]
    extras_pool = [4, 18, 21, 24]

    # Initialize and run the generator
    CombinationsGenerator.generate_combinations(numbers_pool, extras_pool)


def get_results_for_year(year: int):
    """
    Makes an API call to lotto.net for a specific year's results and returns the response as a string.
    """
    try:
        response: str = LottoNetAPI.get_results_for_year(year)
        logging.info(f"Results for year {year}: {re.sub(r'\s+', '', response)}")
    except Exception as e:
        logging.error(f"An error occurred while fetching results for {year}: {e}")


def main():
    generate_combinations()
    get_results_for_year(2025)


if __name__ == "__main__":
    main()
