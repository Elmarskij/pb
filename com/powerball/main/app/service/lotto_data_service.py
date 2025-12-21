import logging
from com.powerball.main.rest.lotto_net import LottoNetAPI
from com.powerball.main.utility.common_utilities import CommonUtilities


class LottoDataService:
    """
    Service class to handle the orchestration of fetching and parsing lottery data.
    """

    @staticmethod
    def fetch_and_parse_yearly_results(year: int) -> list[dict[str, list[int]]]:
        """
        Fetches the lottery results page for a given year and parses it.
        """
        try:
            logging.info(f"Requesting results for the year {year}.")
            html_content = LottoNetAPI.get_results_for_year(year)
            if not html_content:
                logging.warning(f"No HTML content was returned for the year {year}.")
                return []

            return CommonUtilities.parse_annual_results(html_content, year)
        except Exception as e:
            logging.error(f"Critical error fetching/parsing results for {year}: {e}", exc_info=True)
            return []

    @classmethod
    def fetch_all_historical_results(cls) -> dict[int, list[list[int]]]:
        """
        Fetches all historical lottery results for the defined range (2025-2015).
        """
        all_results = {}
        # Fetches results from 2025 down to 2015.
        for year in range(2025, 2014, -1):
            all_results[year] = cls.fetch_and_parse_yearly_results(year)
        return all_results