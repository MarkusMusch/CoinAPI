""" This module contains functions that generate graphs for the funding rates and stable coin interest. """
import numpy as np

from backend.data_access.crud.crud_funding import read_funding_entries
from backend.data_access.crud.crud_interest import read_interest_entries
from backend.models.models_orm import Coin, Symbol


def load_data_cumulative_funding_leveraged(
    symbol: Symbol = Symbol.BTCUSDT.value,
    stablecoin: Coin = Coin.DAI.value
):
    """ This function loads the data for the cumulative funding rate graph.

    Args:
        symbol (Symbol, optional): The symbol for which the cumulative return should be calculated.
            Defaults to Symbol.BTCUSDT.value.
        stablecoin (Coin, optional): The stable coin for which the interest rates should be calculated.
    
    Returns:
        dict: A dictionary containing the timestamps and funding rates for the given coin.
    """
    timestamps_coin, funding_rates_coin = read_funding_entries(Symbol(symbol), num_values=3*365)
    timestamps_stable, interest_rates_stable = read_interest_entries(Coin(stablecoin))
    first_entry = max(min(timestamps_coin), min(timestamps_stable))

    interest_rates_stable = interest_rates_stable[len(interest_rates_stable) % 8:].reshape(-1, 8).sum(axis=1)
    timestamps_stable = timestamps_stable[len(timestamps_stable) % 8::8]

    timestamps_stable = [timestamp for timestamp in timestamps_stable if timestamp >= first_entry]
    timestamps_coin = [timestamp for timestamp in timestamps_coin if timestamp >= first_entry][-len(timestamps_stable):]

    funding_rates_coin = funding_rates_coin[-len(timestamps_coin):]
    interest_rates_stable = interest_rates_stable[-len(timestamps_stable):]
    
    compound_funding_coin = 100*(np.cumprod(1 + np.array(funding_rates_coin)) - 1)
    compound_interest_stable = 100*(np.cumprod(1 + np.array(interest_rates_stable)) - 1)
    compound_difference = 100*(np.cumprod(1 + np.array(funding_rates_coin) - np.array(interest_rates_stable)) - 1)

    title = f"{symbol} Funding Rate Cumulative"

    data = []
    for ts, compound, linear, difference in zip(timestamps_coin, compound_funding_coin, compound_interest_stable, compound_difference):
        data.append(
            {
                "date": ts.strftime("%b %y"),
                f"Compound Funding {symbol}": round(compound, 2),
                f"Compound Interest {stablecoin}": round(linear, 2),
                "Compound Difference": round(difference, 2)
            }
        )
    
    series = [
        {"name": f"Compound Funding {symbol}", "color": "blue.6"},
        {"name": f"Compound Interest {stablecoin}", "color": "orange.6"},
        {"name": "Compound Difference", "color": "green.6"}
    ]
    
    return title, data, series


def load_data_funding_rates_leveraged(
    symbol: Symbol = Symbol.BTCUSDT.value,
    stablecoin: Coin = Coin.DAI.value
):
    """ This function loads the data for the funding rate graph.

    Args:
        symbol (Symbol, optional): The symbol for which the funding rates should be calculated.
            Defaults to Symbol.BTCUSDT.value.
        stablecoin (Coin, optional): The stable coin for which the interest rates should be calculated.
    
    Returns:
        dict: A dictionary containing the timestamps and funding rates for the given coin.
    """
    timestamps_coin, funding_rates_coin = read_funding_entries(Symbol(symbol), num_values=None)
    timestamps_stable, interest_rates_stable = read_interest_entries(Coin(stablecoin))
    first_entry = max(min(timestamps_coin), min(timestamps_stable))

    interest_rates_stable = interest_rates_stable[len(interest_rates_stable) % 8:].reshape(-1, 8).sum(axis=1)
    timestamps_stable = timestamps_stable[len(timestamps_stable) % 8::8]

    timestamps_stable = [timestamp for timestamp in timestamps_stable if timestamp >= first_entry]
    timestamps_coin = [timestamp for timestamp in timestamps_coin if timestamp >= first_entry][-len(timestamps_stable):]

    funding_rates_coin = 100*(funding_rates_coin[-len(timestamps_coin):])
    interest_rates_stable = 100*(interest_rates_stable[-len(timestamps_stable):])

    title = f"{symbol} Funding Rate vs. Interest"

    data = []
    for ts, funding, interest in zip(
        timestamps_coin,
        funding_rates_coin,
        interest_rates_stable
    ):
        data.append(
            {
                "date": ts.strftime('%b %y'),
                f"Funding {symbol}": round(funding, 5),
                f"Interest {stablecoin}": round(interest, 5)
            }
        )
    
    series = [
        {"name": f"Funding {symbol}", "color": "blue.6"},
        {"name": f"Interest {stablecoin}", "color": "orange.6"}
    ]

    return title, data, series


def load_data_net_income_leveraged(
    symbol: Symbol = Symbol.BTCUSDT.value,
    stablecoin: Coin = Coin.DAI.value
):
    """ This function loads the data for the net income graph.

    Args:
        symbol (Symbol, optional): The symbol for which the net income should be calculated.
            Defaults to Symbol.BTCUSDT.value
        stablecoin (Coin, optional): The stable coin for which the interest rates should be calculated.
    
    Returns:
        dict: A dictionary containing the timestamps and net income for the given coin.
    """
    timestamps_coin, funding_rates_coin = read_funding_entries(Symbol(symbol), num_values=None)
    timestamps_stable, interest_rates_stable = read_interest_entries(Coin(stablecoin))
    first_entry = max(min(timestamps_coin), min(timestamps_stable))

    interest_rates_stable = interest_rates_stable[len(interest_rates_stable) % 8:].reshape(-1, 8).sum(axis=1)
    timestamps_stable = timestamps_stable[len(timestamps_stable) % 8::8]

    timestamps_stable = [timestamp for timestamp in timestamps_stable if timestamp >= first_entry]
    timestamps_coin = [timestamp for timestamp in timestamps_coin if timestamp >= first_entry][-len(timestamps_stable):]

    funding_rates_coin = 100*(funding_rates_coin[-len(timestamps_coin):])
    interest_rates_stable = 100*(interest_rates_stable[-len(timestamps_stable):])

    net_income = np.array(funding_rates_coin) - np.array(interest_rates_stable)
    window_size = 30
    moving_average_30d = np.convolve(net_income, np.ones(window_size) / window_size, mode='valid')

    title = f"{symbol} Net Income"

    data = []
    for ts, income, ma30 in zip(
        timestamps_coin[-len(moving_average_30d):],
        net_income[-len(moving_average_30d):],
        moving_average_30d
    ):
        data.append(
            {
                "date": ts.strftime("%b %y"),
                "Difference": round(income, 5),
                "Moving Average 30d": round(ma30, 5)
            }
        )
    
    series = [
        {"name": "Difference", "color": "green.6"},
        {"name": "Moving Average 30d", "color": "red.6"}
    ]

    return title, data, series