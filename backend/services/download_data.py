from datetime import datetime, timezone
import logging
import time

from backend.data_access.api_client.bybit_client import ByBitClient
from backend.data_access.crud.crud_funding import create_funding_entries
from backend.data_access.crud.crud_interest import create_interest_entries
from backend.data_access.crud.crud_open_interest import create_open_interest_entries
from backend.models.models_api import FundingRequest, OpenInterestRequest
from backend.models.models_orm import Coin, FundingRate, InterestRate, OpenInterest, Symbol


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def catch_latest_funding(
    client: ByBitClient,
    symbol: Symbol,
    most_recent_datetime: str
) -> None:
    
    now = int(datetime.now(timezone.utc).timestamp() * 1000)
    end_time = now

    most_recent_time = most_recent_datetime.timestamp() * 1000

    if most_recent_time < now - 8*60*60*1000:

        category = "linear"

        while end_time > most_recent_time:
            data = client.get_funding_history(
                FundingRequest(
                    category=category,
                    symbol=symbol,
                    endTime=now
                )
            )

            for item in data.list:
                funding_rate_record = FundingRate(
                    symbol=symbol.value,
                    funding_rate=item.fundingRate,
                    funding_rate_timestamp=item.fundingRateTimestamp
                )
                create_funding_entries(funding_rate_record=funding_rate_record)

            end_time -= min(30*60*60*1000, end_time - most_recent_time)


def catch_latest_open_interest(
    client: ByBitClient,
    symbol: Symbol,
    most_recent_datetime: str
) -> None:

    now = int(datetime.now(timezone.utc).timestamp() * 1000)
    end_time = now

    most_recent_time = most_recent_datetime.timestamp() * 1000

    if most_recent_time < now - 8*60*60*1000:

        category = "linear"

        while end_time > most_recent_time:
            data = client.get_open_interest(
                OpenInterestRequest(
                    category=category,
                    symbol=symbol,
                    intervalTime='1h',
                    endTime=now
                )
            )

            for item in data.list:
                open_interest_record = OpenInterest(
                    symbol=symbol.value,
                    open_interest=item.openInterest,
                    open_interest_timestamp=item.timestamp
                )
                create_open_interest_entries(open_interest_record=open_interest_record)

            end_time -= min(30*60*60*1000, end_time - most_recent_time)


def catch_latest_interest(
    client: ByBitClient,
    coin: Coin,
    most_recent_datetime: str
) -> None:

    now = int(datetime.now(timezone.utc).timestamp() * 1000)
    end_time = now

    most_recent_time = most_recent_datetime.timestamp() * 1000

    if most_recent_time < now - 8*60*60*1000:

        while end_time > most_recent_time:
            data = client.get_interest_rate(coin.value, end_time=now)

            for item in data.list:
                interest_rate_record = InterestRate(
                    coin=coin.value,
                    interest_rate=item.hourlyBorrowRate,
                    interest_rate_timestamp=item.timestamp
                )
                create_interest_entries(interest_rate_record=interest_rate_record)

            end_time -= min(30*60*60*1000, end_time - most_recent_time)


def fill_funding(
    client: ByBitClient,
    symbol: Symbol
) -> None:
    category = "linear"

    now = int(time.time() * 1000)
    end_time = now

    while True:

        data = client.get_funding_history(
            FundingRequest(
                category=category,
                symbol=symbol,
                endTime=end_time
            )
        )
        if data.list:
            for item in data.list:
                funding_rate_record = FundingRate(
                    symbol=symbol.value,
                    funding_rate=item.fundingRate,
                    funding_rate_timestamp=item.fundingRateTimestamp
                )
                create_funding_entries(funding_rate_record=funding_rate_record)
            end_time = int(data.list[-1].fundingRateTimestamp) - 1
        else:
            break


def fill_open_interest(
    client: ByBitClient,
    symbol: Symbol
) -> None:
    category = "linear"

    now = int(time.time() * 1000)
    end_time = now

    while True:

        data = client.get_open_interest(
            OpenInterestRequest(
                category=category,
                symbol=symbol.value,
                intervalTime="1h",
                endTime=end_time
                )
            )
        if data.list:
            for item in data.list:
                open_interest_record = OpenInterest(
                    symbol=symbol.value,
                    open_interest=item.openInterest,
                    open_interest_timestamp=item.timestamp
                )
                create_open_interest_entries(open_interest_record=open_interest_record)
            end_time = int(data.list[-1].timestamp) - 1
        else:
            break


def fill_interest(
    client: ByBitClient,
    coin: Coin
) -> None:
    now = int(time.time() * 1000)
    end_time = now

    while True:
        data = client.get_interest_rate(coin.value, end_time=end_time)

        if data.list:
            for item in data.list:
                interest_rate_record = InterestRate(
                    coin=coin.value,
                    interest_rate=item.hourlyBorrowRate,
                    interest_rate_timestamp=item.timestamp
                )
                create_interest_entries(interest_rate_record=interest_rate_record)
            end_time = int(data.list[-1].timestamp) - 1
        else:
            break