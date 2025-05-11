from datetime import datetime, timezone

import numpy as np
from pydantic import ValidationError
import pytest

from backend.models.models_api import (
    FundingHistoryResponse,
    FundingRateItem,
    InterestRateResponse,
    InterestRateItem
)


class TestFundingHistoryResponse:

    def test_funding_rate_item_with_invalid_arguments(self):
        # Case 1: Invalid type for `fundingRate` (should be string)
        with pytest.raises(ValidationError):
            FundingRateItem(fundingRate=123, fundingRateTimestamp="1700000000")
        
        # Case 2: Invalid type for `fundingRateTimestamp` (should be string)
        with pytest.raises(ValidationError):
            FundingRateItem(fundingRate="1.0", fundingRateTimestamp=1700000000)
        
        # Case 3: Missing required fields
        with pytest.raises(ValidationError):
            FundingRateItem(fundingRate="1.0")

    def test_funding_history_response_with_invalid_arguments(self):
        # Case 1: Invalid type for `category` (should be a string)
        with pytest.raises(ValidationError):
            FundingHistoryResponse(category=123, list=[])
        
        # Case 2: Invalid type for `list` (should be a list of FundingRateItem)
        with pytest.raises(ValidationError):
            FundingHistoryResponse(category="crypto", list="not_a_list")

        # Case 3: List contains an invalid item type (e.g., list of integers)
        with pytest.raises(ValidationError):
            FundingHistoryResponse(category="crypto", list=[123, 456])

    def test_unpack_data(self):
        funding_rate_item1 = FundingRateItem(fundingRate='1', fundingRateTimestamp='1700000000000')
        funding_rate_item2 = FundingRateItem(fundingRate='2', fundingRateTimestamp='1700000100000')

        funding_rate_response = FundingHistoryResponse(category="linear",
                                                       list=[funding_rate_item1, funding_rate_item2])
        
        timestamps, funding_rates = funding_rate_response.unpacked_data

        expected_datetimes = [
            datetime(2023, 11, 14, 22, 15, tzinfo=timezone.utc),
            datetime(2023, 11, 14, 22, 13, 20 ,tzinfo=timezone.utc)
        ]
        expected_funding_rates = [2.0, 1.0]

        assert list(timestamps) == expected_datetimes
        assert list(funding_rates) == expected_funding_rates

    def test_cumulative_return(self):
        # Define two sample funding rate items
        funding_rate_item1 = FundingRateItem(fundingRate='1', fundingRateTimestamp='1700000000000')
        funding_rate_item2 = FundingRateItem(fundingRate='2', fundingRateTimestamp='1700000100000')

        # Create the FundingHistoryResponse object
        funding_rate_response = FundingHistoryResponse(category="linear",
                                                    list=[funding_rate_item1, funding_rate_item2])

        # Get the cumulative return from the property
        cumulative_return = funding_rate_response.cumulative_return

        # Expected cumulative return calculation:
        # Step 1: funding rates are [2.0, 1.0]
        # Step 2: cumulative return calculation:
        #         (1 + 2.0) * (1 + 1.0) - 1 = 3.0 * 2.0 - 1 = 6.0 - 1 = 5.0
        expected_cumulative_return = np.array([2.0, 5.0])

        # Assert that the cumulative return is as expected
        np.testing.assert_array_almost_equal(cumulative_return, expected_cumulative_return)


class TestInterestRateResponse:

    def test_interest_rate_item_with_invalid_arguments(self):
        # Case 1: Invalid type for `hourlyBorrowRate` (should be string)
        with pytest.raises(ValidationError):
            InterestRateItem(hourlyBorrowRate=1.0, timestamp=1700000000)

        # Case 2: Invalid type for `timestamp` (should be an integer)
        with pytest.raises(ValidationError):
            InterestRateItem(hourlyBorrowRate="0.05", timestamp="invalid_timestamp")

        # Case 3: Missing required fields
        with pytest.raises(ValidationError):
            InterestRateItem(hourlyBorrowRate="0.05")

    def test_interest_rate_response_with_invalid_arguments(self):
        # Case 1: Invalid type for `list` (should be a list of InterestRateItem)
        with pytest.raises(ValidationError):
            InterestRateResponse(list="not_a_list")

        # Case 2: List contains invalid item type (e.g., integers instead of InterestRateItem)
        with pytest.raises(ValidationError):
            InterestRateResponse(list=[123, 456])

    def test_unpack_data(self):
        # Create sample InterestRateItems
        interest_rate_item1 = InterestRateItem(hourlyBorrowRate='0.05', timestamp=1700000000000)
        interest_rate_item2 = InterestRateItem(hourlyBorrowRate='0.03', timestamp=1700000100000)

        # Create InterestRateResponse object
        interest_rate_response = InterestRateResponse(list=[interest_rate_item1, interest_rate_item2])

        # Unpack data
        timestamps, interest_rates = interest_rate_response.unpacked_data

        # Expected datetime and interest rates
        expected_datetimes = [
            datetime(2023, 11, 14, 22, 15, tzinfo=timezone.utc),
            datetime(2023, 11, 14, 22, 13, 20, tzinfo=timezone.utc)
        ]
        expected_interest_rates = [0.03, 0.05]

        # Assertions for unpacked data
        assert list(timestamps) == expected_datetimes
        assert list(interest_rates) == expected_interest_rates

    def test_cumulative_return(self):
        # Create sample InterestRateItems
        interest_rate_item1 = InterestRateItem(hourlyBorrowRate='1.0', timestamp=1700000000000)
        interest_rate_item2 = InterestRateItem(hourlyBorrowRate='2.0', timestamp=1700000100000)

        # Create InterestRateResponse object
        interest_rate_response = InterestRateResponse(list=[interest_rate_item1, interest_rate_item2])

        # Calculate cumulative return
        cumulative_return = interest_rate_response.cumulative_return

        # Expected cumulative return calculation:
        # Step 1: funding rates are [2.0, 1.0]
        # Step 2: cumulative return calculation:
        #         (1 + 2.0) * (1 + 1.0) - 1 = 3.0 * 2.0 - 1 = 6.0 - 1 = 5.0
        expected_cumulative_return = np.array([2.0, 5.0])

        # Assert that the cumulative return is as expected
        np.testing.assert_array_almost_equal(cumulative_return, expected_cumulative_return)