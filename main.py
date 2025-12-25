import logging
import streamlit as st

# Import the new service and app runner
from com.powerball.main.app.service.lotto_data_service import LottoDataService
from com.powerball.main.app.dashboard_app import run_dashboard
# Import combinations runner (for future use)
from com.powerball.main.app.combinatorics.combinations_runner import generate_combinations_csv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)


@st.cache_data
def get_cached_historical_data():
    """
    Streamlit Caching Wrapper.
    Calls the business logic in LottoDataService, but wraps it 
    so Streamlit doesn't re-run it on every button click.
    """
    logging.info("cache miss: Fetching fresh data from API...")
    return LottoDataService.fetch_all_historical_results()


def main():
    """The main entry point of the script."""
    logging.info("Starting the Powerball Dashboard.")

    # # 1. Business Action: Get Data (Cached)
    # historical_data = get_cached_historical_data()
    #
    # logging.info(f"Data ready for {len(historical_data)} games.")
    # logging.info(f"historical_data: {historical_data}")
    #
    # # 2. Business Action: Run Dashboard
    # run_dashboard(historical_data)

    # Future Use:
    generate_combinations_csv()


if __name__ == "__main__":
    main()
