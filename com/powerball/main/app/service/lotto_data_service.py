import logging
import pandas as pd
from datetime import datetime
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
    def fetch_all_historical_results(cls) -> pd.DataFrame:
        """
        Fetches data and returns a FLAT PANDAS DATAFRAME.
        Columns: ['Date', 'n1', 'n2', 'n3', 'n4', 'n5', 'pb']
        """
        all_draws = []

        # 1. Fetch Loop
        for year in range(2025, 2014, -1):
            year_data = cls.fetch_and_parse_yearly_results(year)

            # 2. Flatten the structure immediately
            for draw_record in year_data:
                for date_str, numbers in draw_record.items():
                    # Parse date ONCE here
                    try:
                        dt = datetime.strptime(date_str, "%m-%d-%Y")
                        # Ensure we have enough numbers
                        if len(numbers) >= 6:
                            row = {
                                'Date': dt,
                                'n1': numbers[0], 'n2': numbers[1], 'n3': numbers[2],
                                'n4': numbers[3], 'n5': numbers[4],
                                'pb': numbers[5]
                            }
                            all_draws.append(row)
                    except ValueError:
                        continue

        # 3. Create DataFrame
        df = pd.DataFrame(all_draws)

        # Sort by date for safety
        if not df.empty:
            df = df.sort_values(by='Date', ascending=False)

        logging.info(f"Converted {len(df)} rows into DataFrame.")
        return df
