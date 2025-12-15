# lotto_net.py
import logging
import re
from typing import Final
import requests
from requests import Response


class LottoNetAPI:
    """
    Handles API calls to lotto.net to retrieve lottery results.
    """

    _BASE_URL: Final[str] = "https://www.lotto.net/ru/powerball/rezultaty/"
    _HEADERS: Final[dict[str, str]] = {'Cookie': 'PromoShown=True'}

    @classmethod
    def get_results_for_year(cls, year: int) -> str:
        """
        Makes an API call to lotto.net for a specific year's results and returns the response as a string.

        Args:
            year: The year for which to retrieve the lottery results.

        Returns:
            The content of the API response as a string.
        """
        url: str = f"{cls._BASE_URL}{year}"
        try:
            response: Response = requests.get(url, headers=cls._HEADERS)
            response.raise_for_status()  # Raise an exception for HTTP errors
            logging.info(f"Successfully retrieved data from {url}")
            return re.sub(r'\s+', '', response.text)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error making API call to {url}: {e}")
            return ""
