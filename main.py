# main_script.py
import logging

from com.powerball.main.app.combinations_generator import CombinationsGenerator
from com.powerball.main.rest.lotto_net import LottoNetAPI
from com.powerball.main.utility.common_utilities import CommonUtilities

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


def get_results_for_year(year: int) -> list[list[int]]:
    """ Fetch annual draw results """
    try:
        response: str = LottoNetAPI.get_results_for_year(year)
        annual_number_2025: list[list[int]] = CommonUtilities.fetch_annual_draw_result(response)
        return annual_number_2025
    except Exception as e:
        logging.error(f"An error occurred while fetching results for {year}: {e}")
        return [[]]

def get_results() -> dict[int, list[list[int]]]:
    """ Fetch all results """
    results: dict[int, list[list[int]]] = {}
    for i in range(2025, 2015 - 1, -1):
        results[i] = get_results_for_year(i)
    return results


def main():
    # generate_combinations()
    # get_results_for_year(2025)
    results: dict[int, list[list[int]]] = get_results()
    logging.info(f"Results: {results}")
    logging.info(f"Length of results: {len(results)}")


if __name__ == "__main__":
    main()
