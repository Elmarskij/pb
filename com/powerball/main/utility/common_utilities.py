# common_utilities.py
import logging
import re
from typing import Optional

import dateparser


class CommonUtilities:
    """A utility class for parsing lottery draw results from HTML content."""

    _properties: Optional[dict[str, str]] = None

    @classmethod
    def parse_annual_results(cls, dom: str, year: int) -> list[dict[str, list[int]]]:
        """
        Parses the HTML content for a given year to extract all lottery draw results.

        Args:
            dom: The HTML content string for a full year's lottery results.
            year: The year being parsed, used for special date handling.

        Returns:
            A list of lists, where each inner list contains the numbers for a single draw.
        """
        logging.info(f"Parsing lottery results for the year {year} from the provided HTML content.")

        all_draws_html = cls._extract_all_draws_html(dom)
        
        parsed_draws = []
        for draw_html in all_draws_html:
            # This hardcoded date is to handle a known format change on the website for older results.
            draw_date_str = cls._extract_date_from_draw_html(draw_html)
            if year == 2015 and draw_date_str == '10-03-2015':
                logging.warning("Stopping parsing for 2015 before 10-03-2015 due to a rule change in 10-07-2025")
                break

            raw_numbers_html = cls._extract_raw_numbers_from_draw_html(draw_html)
            numbers = cls._parse_numbers_from_html_spans(raw_numbers_html)
            if numbers:
                parsed_draws.append({draw_date_str: numbers})
        
        return parsed_draws

    @classmethod
    def _convert_russian_date(cls, russian_date: str) -> str:
        """
        Converts a date string in Russian to a standard 'MM-DD-YYYY' format.

        Args:
            russian_date: The date string, potentially in Russian.

        Returns:
            The formatted date string.
        """
        return dateparser.parse(russian_date).date().strftime("%m-%d-%Y")

    @classmethod
    def _extract_all_draws_html(cls, dom: str) -> list[str]:
        """
        Extracts HTML segments for each individual draw from the annual HTML content.

        Args:
            dom: The complete HTML content for a year.

        Returns:
            A list of HTML strings, each corresponding to a single draw.
        """
        pattern = cls.get_from_config("annual_draw_pattern")
        return re.findall(pattern, dom)

    @classmethod
    def _extract_raw_numbers_from_draw_html(cls, draw_html: str) -> list[str]:
        """
        Extracts the raw HTML for the winning numbers from a single draw's HTML.

        Args:
            draw_html: The HTML content for a single draw.

        Returns:
            A list of raw HTML strings for each number. The 'PowerPlay' number is excluded.
        """
        ball_pattern = cls.get_from_config("daily_draw_pattern")
        raw_numbers = re.findall(ball_pattern, draw_html)
        
        # The last number found is the 'PowerPlay' multiplier, which is not a winning number.
        if raw_numbers:
            raw_numbers.pop()

        return raw_numbers

    @classmethod
    def _parse_numbers_from_html_spans(cls, raw_numbers_html: list[str]) -> list[int]:
        """
        Parses a list of raw HTML number spans into a list of integers.

        Args:
            raw_numbers_html: A list of HTML strings, e.g., ['<span>10</span>', '<span>20</span>'].

        Returns:
            A list of the extracted numbers as integers.
        """
        # This list comprehension is a fast way to clean the HTML tags and convert to int.
        return [int(span.replace('<span>', '').replace('</span>', '')) for span in raw_numbers_html]

    @classmethod
    def _extract_date_from_draw_html(cls, draw_html: str) -> str:
        """
        Extracts and formats the draw date from a single draw's HTML content.

        Args:
            draw_html: The HTML content for a single draw.

        Returns:
            The formatted date string ('MM-DD-YYYY').
        """
        draw_date_pattern = cls.get_from_config("draw_date_pattern")
        match = re.search(draw_date_pattern, draw_html)
        if not match:
            return ""
            
        raw_date = match.group().replace('</span>', '').replace('</div>', '')
        return cls._convert_russian_date(raw_date)

    @staticmethod
    def get_from_config(key: str) -> Optional[str]:
        """
        Retrieves a configuration value for a given key from 'config.properties'.
        The properties are cached after the first read to improve performance.

        Args:
            key: The configuration key to look up.

        Returns:
            The configuration value as a string, or None if not found.
        """
        if CommonUtilities._properties is None:
            logging.info("Loading properties from config.properties for the first time.")
            CommonUtilities._properties = CommonUtilities._load_properties()
        return CommonUtilities._properties.get(key)

    @staticmethod
    def _load_properties() -> dict[str, str]:
        """
        Reads the 'config.properties' file and returns its contents as a dictionary.

        Returns:
            A dictionary containing the key-value pairs from the properties file.
        """
        filepath = "config.properties"
        properties = {}
        try:
            with open(filepath, "rt") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key_value = line.split('=', 1)
                        if len(key_value) == 2:
                            properties[key_value[0].strip()] = key_value[1].strip()
        except FileNotFoundError:
            logging.error(f"Configuration file not found: {filepath}")
            return {}
        return properties
