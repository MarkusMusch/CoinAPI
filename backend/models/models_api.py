""" This module contains the Pydantic models for the API endpoints. """
from datetime import datetime, timezone
import numpy as np
from pydantic import BaseModel
from typing import List, Tuple


class FundingRequest(BaseModel):
    """A Pydantic model for the funding history request."""
    category: str
    symbol: str
    endTime: int


class FundingRateItem(BaseModel):
    """A Pydantic model for a single funding rate item."""
    fundingRate: str
    fundingRateTimestamp: str


class FundingHistoryResponse(BaseModel):
    """A Pydantic model for the funding history response."""
    category: str
    list: List[FundingRateItem]

    @property
    def unpacked_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Unpack the data from the response."""
        # Convert timestamps to datetime objects
        timestamps = np.array([datetime.fromtimestamp(int(item.fundingRateTimestamp) / 1000, tz=timezone.utc) for item in self.list])[::-1]
        funding_rates = np.array([float(item.fundingRate) for item in self.list])[::-1]
        return timestamps, funding_rates

    @property
    def cumulative_return(self) -> np.ndarray:
        """Calculate the cumulative return from the funding rates."""
        # Calculate cumulative return
        _, funding_rates = self.unpacked_data
        return np.cumprod(1 + funding_rates) - 1


class OpenInterestRequest(BaseModel):
    """A Pydantic model for the open interest request."""
    category: str
    symbol: str
    intervalTime: str
    endTime: int


class OpenInterestItem(BaseModel):
    """A Pydantic model for a single open interest item."""
    openInterest: str
    timestamp: str


class OpenInterestResponse(BaseModel):
    """A Pydantic model for the open interest response."""
    category: str
    list: List[OpenInterestItem]


class InterestRateItem(BaseModel):
    """A Pydantic model for a single interest rate item."""
    hourlyBorrowRate: str
    timestamp: int


class InterestRateResponse(BaseModel):
    """A Pydantic model for the interest rate response."""
    list: List[InterestRateItem]

    @property
    def unpacked_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Unpack the data from the response."""
        datetimes = np.array([datetime.fromtimestamp(int(item.timestamp) / 1000, tz=timezone.utc) for item in self.list])[::-1]
        interest_rates = np.array([float(item.hourlyBorrowRate) for item in self.list])[::-1]
        return datetimes, interest_rates
    
    @property
    def cumulative_return(self) -> np.ndarray:
        """Calculate the cumulative return from the interest rates."""
        _, interest_rates = self.unpacked_data
        return np.cumprod(1 + interest_rates) - 1