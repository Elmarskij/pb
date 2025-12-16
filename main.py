# main_script.py
import logging
import streamlit as st

from com.powerball.main.app.combinatorics.combinations_generator import CombinationsGenerator
from com.powerball.main.rest.lotto_net import LottoNetAPI
from com.powerball.main.utility.common_utilities import CommonUtilities
from com.powerball.main.app.charts.frequency_bar import run_dashboard, FrequencyChartGenerator

# Configure logging to provide detailed output, including timestamps and file context.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)


def generate_combinations():
    """Main execution function to run the process."""

    # Define the input data pools here
    numbers_pool = [10, 21, 23, 28, 32, 33, 39, 61, 62, 63, 64, 69]
    extras_pool = [4, 18, 21, 24]

    CombinationsGenerator.generate_combinations(numbers_pool, extras_pool)

def fetch_and_parse_yearly_results(year: int) -> list[dict[str, list[int]]]:
    """
    Fetches the lottery results page for a given year and parses it to extract the winning numbers.

    Args:
        year: The year to fetch results for.

    Returns:
        A list of lists, where each inner list contains the winning numbers for a single draw.
        Returns an empty list if an error occurs.
    """
    try:
        logging.info(f"Requesting results for the year {year}.")
        html_content = LottoNetAPI.get_results_for_year(year)
        if not html_content:
            logging.warning(f"No HTML content was returned for the year {year}.")
            return []
            
        return CommonUtilities.parse_annual_results(html_content, year)
    except Exception as e:
        logging.error(f"A critical error occurred while fetching or parsing results for {year}: {e}", exc_info=True)
        return []

def fetch_all_historical_results() -> dict[int, list[list[int]]]:
    """
    Fetches all historical lottery results for a predefined range of years.

    Returns:
        A dictionary where keys are years and values are the lists of winning numbers for that year.
    """
    all_results = {}
    # Fetches results from 2025 down to 2015.
    for year in range(2025, 2014, -1):
        all_results[year] = fetch_and_parse_yearly_results(year)
    return all_results

def generate_general_frequency_chart(input_data: dict[int, list[list[int]]]) -> None:
    # 1. Instantiate the generator class with your data
    chart_gen = FrequencyChartGenerator(input_data)

    # 2. Generate the chart for the "Main Numbers" (First 5 balls)
    chart_gen.plot(plot_type='main')

    # 3. Generate the chart for the "Special Ball" (The 6th ball)
    chart_gen.plot(plot_type='special')

@st.cache_data
def get_cached_historical_data():
    """
    Wraps the API call with caching.
    Streamlit will run this ONCE, store the result,
    and just return the result instantly on subsequent runs.
    """
    logging.info("cache miss: Fetching fresh data from API...")
    return fetch_all_historical_results()

def main():
    """The main entry point of the script."""
    logging.info("Starting the Powerball results fetching process.")
    
    historical_data = get_cached_historical_data()
    
    logging.info(f"Successfully fetched results for {len(historical_data)} years.")
    # Example of how to access and print the results for a specific year.
    if 2025 in historical_data:
        logging.info(f"First 5 results for 2025: {historical_data[2025][:5]}")
    # logging.info(f"Results: {historical_data}")

    run_dashboard(historical_data)

if __name__ == "__main__":
    main()
