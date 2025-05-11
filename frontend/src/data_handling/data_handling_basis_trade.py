""" This module contains functions that generate graphs for the funding rates and stable coin interest. """
import numpy as np

from backend.data_access.crud.crud_funding import read_funding_entries
from backend.models.models_orm import Symbol


def load_data_cumulative_funding(symbol: Symbol = Symbol.BTCUSDT.value):
    """ This function loads the data for the cumulative funding rate graph.

    Args:
        symbol (Symbol, optional): The symbol for which the cumulative return should be calculated.
            Defaults to Symbol.BTCUSDT.value.
    
    Returns:
        dict: A dictionary containing the timestamps and funding rates for the given coin.
    """
    timestamps_coin, funding_rates_coin = read_funding_entries(Symbol(symbol), num_values=5*3*365)
    linear_return_coin = 100 * np.cumsum(np.array(funding_rates_coin))
    cumulative_return_btc = 100 * (np.cumprod(1 + np.array(funding_rates_coin)) - 1)

    title = f"{symbol} Funding Rate Cumulative"
    data = []
    for ts, compound, linear in zip(timestamps_coin, cumulative_return_btc, linear_return_coin):
        data.append(
            {
                'date': ts.strftime('%b %y'),
                f'Compound Funding {symbol}': round(compound, 2),
                f'Cummulative Funding {symbol}': round(linear, 2)
            }
        )
    
    series = [
        {"name": f"Compound Funding {symbol}", "color": "indigo.6"},
        {"name": f"Cummulative Funding {symbol}", "color": "blue.6"}
    ]
    
    return title, data, series


def load_data_funding_rates(symbol: Symbol = Symbol.BTCUSDT.value):
    """ This function loads the data for the funding rate graph.

    Args:
        symbol (Symbol, optional): The symbol for which the funding rates should be calculated.
            Defaults to Symbol.BTCUSDT.value.
    
    Returns:
        dict: A dictionary containing the timestamps and funding rates for the given coin.
    """
    timestamps_btc, funding_rates_btc = read_funding_entries(Symbol(symbol), num_values=5*3*365)

    title = f"{symbol} Funding Rate"
    
    data = []
    for ts, value in zip(timestamps_btc, funding_rates_btc):
        data.append({'date': ts.strftime('%b %y'), f'Funding {symbol}': round(100*value, 5)})
    
    series = [
        {"name": f"Funding {symbol}", "color": "blue.6"},
    ]

    return title, data, series
