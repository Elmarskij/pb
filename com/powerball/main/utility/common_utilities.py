#common_utilities.py
import logging
import re

import dateparser


class CommonUtilities:

    @classmethod
    def fetch_annual_draw_result(cls, dom: str) -> list[list[int]]:
        logging.info("Fetching draw_numbers from the provided HTML content.")

        annual_number = []
        annual_raw_draw_details: list[str] = CommonUtilities._fetch_raw_annual_draw_results(dom)

        for annual_raw_draw_detail in annual_raw_draw_details:
            daily_draw_detail: dict[str, list[int]] = CommonUtilities._fetch_daily_draw_results(annual_raw_draw_detail)
            annual_number.append(daily_draw_detail)

        return annual_number

    @classmethod
    def _convert_russian_date(cls, russian_date: str) -> str:
        return dateparser.parse(russian_date).date().strftime("%m-%d-%Y")

    @classmethod
    def _fetch_raw_annual_draw_results(cls, data: str) -> list[str]:
        # Pattern to find annual draw results in the DOM
        pattern = CommonUtilities.get_from_config("annual_draw_pattern")
        # Find all annual draw details
        return re.findall(pattern, data)

    @classmethod
    def _fetch_daily_draw_results(cls, data: str) -> dict[str, list[int]]:
        # Pattern to find daily draw results in the DOM
        ball_pattern: str = CommonUtilities.get_from_config("daily_draw_pattern")
        # Find all daily draw numbers
        daily_raw_draw_numbers: list[str] = re.findall(ball_pattern, data)
        # Pop last element (PowerPlay)
        daily_raw_draw_numbers.pop()
        # Store daily draw numbers in the list
        daily_draw_numbers: list[int] = [int(number.replace('<span>', '').replace('</span>', '')) for number in daily_raw_draw_numbers]

        # Pattern to find draw date
        draw_date_pattern: str = CommonUtilities.get_from_config("draw_date_pattern")
        # Find draw date
        draw_date: str = re.search(draw_date_pattern, data).group().replace('</span>', '').replace('</div>', '')

        return {CommonUtilities._convert_russian_date(draw_date): daily_draw_numbers}

    @staticmethod
    def get_from_config(key: str) -> str:
        return CommonUtilities._load_properties().get(key)

    @staticmethod
    def _load_properties() -> dict[str, str]:
        """
        Reads a properties file and returns a dictionary.
        :return: dict[str, str]
        """
        filepath: str = "config.properties"
        properties: dict[str, str] = {}
        try:
            with open(filepath, "rt") as f:
                for line in f:
                    l = line.strip()
                    # Skip empty lines and comments
                    if l and not l.startswith('#'):
                        # Split only on the first occurrence of the separator
                        key_value = l.split('=', 1)
                        if len(key_value) == 2:
                            key = key_value[0].strip()
                            value = key_value[1].strip()
                            properties[key] = value
        except FileNotFoundError:
            print(f"Error: The file {filepath} was not found.")
            return {}

        return properties
