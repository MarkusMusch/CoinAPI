""" This module contains the API client for the ByBit exchange. 

It provides methods to get the funding history, open interest, and interest rate history from the ByBit API.
"""

import hashlib
import hmac
import requests
from requests.exceptions import RequestException
import time
import logging

from backend.models.models_api import (
    FundingHistoryResponse,
    FundingRequest,
    InterestRateResponse,
    OpenInterestRequest,
    OpenInterestResponse
)
from backend.settings import backend_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ByBitClient:
    """A client to interact with the ByBit exchange API.

    Attributes:
        api_key (str): The API key for the ByBit exchange.
        api_secret (str): The API secret for the ByBit exchange.
        base_endpoint (str): The base endpoint for the ByBit exchange API.
        endpoint_funding (str): The endpoint for the funding history API.
        endpoint_open_interest (str): The endpoint for the open interest API.
        endpoint_interest (str): The endpoint for the interest rate history
            API.
    """

    def __init__(self) -> None:
        self.api_key = backend_settings.BYBIT_API_KEY
        self.api_secret = backend_settings.BYBIT_API_SECRET

        self.base_endpoint = backend_settings.BASE_ENDPOINT_BYBIT
        self.endpoint_funding = backend_settings.ENDPOINT_FUNDING_BYBIT
        self.endpoint_open_interest = backend_settings.ENDPOINT_OPEN_INTEREST_BYBIT
        self.endpoint_interest = backend_settings.ENDPOINT_INTNEREST_BYBIT

        logger.info("ByBitClient initialized with base endpoint %s", self.base_endpoint)

    def _sign_request(self, params: dict) -> str:
        """
        Generate a signature for the given parameters.

        Args:
            params (dict): Parameters for the API request.

        Returns:
            str: The generated HMAC SHA256 signature.

        Raises:
            Exception: If an unexpected error occurs.
        """
        try:
            param_str = '&'.join([f"{key}={value}" for key, value in sorted(params.items())])
            logger.debug("Signing request with")
            signature = hmac.new(self.api_secret.encode('utf-8'), param_str.encode('utf-8'), hashlib.sha256).hexdigest()
            logger.debug("Generated signature")
            return signature
        except Exception as e:
            logger.error("Unexpected error while signing request: %s", e)
            raise
    
    def get_interest_rate(self, currency: str, end_time: int) -> InterestRateResponse:
        """
        Get the interest rate history for the given currency from the exchange API.
        
        Args:
            currency (str): The currency for which to get the interest rate history.
            end_time (int): The end time of the interest rate history.
            
        Returns:
            InterestRateResponse: The interest rate history for the given currency.

        Raises:
            RequestException: If a network error occurs.
            Exception: If an unexpected error occurs.
        """
        url = self.base_endpoint + self.endpoint_interest

        milliseconds_per_day = 24*60*60*1000

        params = {
            "api_key": self.api_key,
            "timestamp":  int(time.time() * 1000),
            "currency": currency,
            "startTime": end_time - 30*milliseconds_per_day,
            "endTime": end_time
        }

        try:
            logger.info("Fetching interest rate for currency: %s", currency)
            signature = self._sign_request(params)
            params['sign'] = signature

            response = requests.get(url, params=params)
            response.raise_for_status()
            response_data = response.json()['result']
            logger.info("Interest rate data fetched successfully")

            if response_data == {}:
                interestrate_history = InterestRateResponse(list=[])
                logger.info("No interest rate data available")
            else:
                interestrate_history = InterestRateResponse(**response_data)
                logger.info("Interest rate data processed successfully")

            return interestrate_history

        except RequestException as e:
            logger.error("Network error occurred while fetching interest rate data: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error while fetching interest rate data: %s", e)
            raise
    
    def get_funding_history(self, params: FundingRequest) -> FundingHistoryResponse:
        """
        Get the funding history for the given parameters from the exchange API.

        Args:
            params (FundingRequest): The parameters for the funding history request.

        Returns:
            FundingHistoryResponse: The funding history for the given parameters.

        Raises:
            RequestException: If a network error occurs.
            Exception: If an unexpected error occurs.
        """
        
        url = self.base_endpoint + self.endpoint_funding

        try:
            logger.info("Fetching funding history")
            response = requests.get(url, params=params.model_dump())
            response.raise_for_status()
            response_data = response.json()['result']
            logger.info("Funding history data fetched successfully")

            if not response_data['list']:
                funding_history = FundingHistoryResponse(category=params.category, list=[])
                logger.info("No funding history data available")
            else:
                funding_history = FundingHistoryResponse(**response_data)
                logger.info("Funding history data processed successfully")

            return funding_history

        except RequestException as e:
            logger.error("Network error occurred while fetching funding history data: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error while fetching funding history data: %s", e)
            raise

    def get_open_interest(self, params: OpenInterestRequest) -> OpenInterestResponse:
        """
        Get the open interest for the given parameters from the exchange API.

        Args:
            params (OpenInterestRequest): The parameters for the open interest request.

        Returns:
            OpenInterestResponse: The open interest for the given parameters.
        
        Raises:
            RequestException: If a network error occurs.
            Exception: If an unexpected error occurs.
        """

        url = self.base_endpoint + self.endpoint_open_interest

        try:
            logger.info("Fetching open interest")
            response = requests.get(url, params=params.model_dump())
            response.raise_for_status()
            response_data = response.json()['result']
            logger.info("Open interest data fetched successfully")

            if not response_data['list']:
                open_interest = OpenInterestResponse(category=params.category, list=[])
                logger.info("No open interest data available")
            else:
                open_interest = OpenInterestResponse(**response_data)
                logger.info("Open interest data processed successfully")

            return open_interest
        
        except RequestException as e:
            logger.error("Network error occurred while fetching open interest data: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error while fetching open interest data: %s", e)
            raise