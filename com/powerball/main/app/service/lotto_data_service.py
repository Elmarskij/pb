import logging
import pandas as pd
from datetime import datetime, timedelta
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

    @staticmethod
    def _get_latest_draw_year() -> int:
        """
        Calculates the year of the most recent lottery draw (Mon, Wed, Sat).
        """
        now = datetime.now()
        draw_days = [0, 2, 5]  # Mon, Wed, Sat

        for i in range(0, 7):
            check_date = now - timedelta(days=i)
            if check_date.weekday() in draw_days:
                return check_date.year
        return now.year

    @classmethod
    def fetch_all_historical_results(cls) -> pd.DataFrame:
        all_draws = []
        start_year = cls._get_latest_draw_year()

        for year in range(start_year, 2014, -1):
            year_data = cls.fetch_and_parse_yearly_results(year)

            for draw_record in year_data:
                for date_str, numbers in draw_record.items():
                    try:
                        dt = datetime.strptime(date_str, "%m-%d-%Y")
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

        df = pd.DataFrame(all_draws)

        if not df.empty:
            df = df.sort_values(by='Date', ascending=False)

            # Filter out future dates (garbage data protection)
            df = df[df['Date'] <= datetime.now()]

            # Ensure proper datetime format
            if not pd.api.types.is_datetime64_any_dtype(df['Date']):
                df['Date'] = pd.to_datetime(df['Date'])

        logging.info(f"Converted {len(df)} rows into DataFrame.")
        return df
