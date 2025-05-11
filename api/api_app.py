from fastapi import FastAPI, Query
import numpy as np
from typing import Any, Dict, Optional

from backend.data_access.crud.crud_funding import read_funding_entries
from backend.data_access.crud.crud_interest import read_interest_entries
from backend.models.models_orm import Symbol, Coin


app = FastAPI()

@app.get("/")
def read_root() -> Dict[str, str]:
    """
    Root endpoint that returns a simple greeting.

    Returns:
        dict: A greeting message.
    """
    return {"message": "Hello, world!"}


@app.get("/funding_rates")
def get_funding_rates(
    symbol: Symbol = Query(Symbol.BTCUSDT),
    num_values: Optional[int] = Query(3 * 365)
) -> Dict[str, Any]:
    """
    Endpoint to fetch funding rate data for a given symbol.

    Args:
        symbol (Symbol): The trading symbol (e.g., BTCUSDT).
        num_values (int): Number of funding rate entries to retrieve.

    Returns:
        dict: Contains a title and a list of funding rate records.
    """
    timestamps_btc, funding_rates_btc = read_funding_entries(Symbol(symbol), num_values=num_values)

    title = f"{symbol} Funding Rate"
    
    data = []
    for ts, value in zip(timestamps_btc, funding_rates_btc):
        data.append({'date': ts.strftime('%b %y'), f'Funding {symbol.value}': round(100*value, 5)})
    
    return {"title": title, "data": data}


@app.get("/funding_rates_cumulative")
def get_funding_rates_cumulative(
    symbol: Symbol = Query(Symbol.BTCUSDT),
    num_values: Optional[int] = Query(3 * 365)
) -> Dict[str, Any]:
    """
    Endpoint to fetch funding rate data for a given symbol.

    Args:
        symbol (Symbol): The trading symbol (e.g., BTCUSDT).
        num_values (int): Number of funding rate entries to retrieve.

    Returns:
        dict: Contains a title and a list of funding rate records.
    """
    timestamps_coin, funding_rates_coin = read_funding_entries(Symbol(symbol), num_values=num_values)
    linear_return_coin = 100 * np.cumsum(np.array(funding_rates_coin))
    cumulative_return_btc = 100 * (np.cumprod(1 + np.array(funding_rates_coin)) - 1)

    title = f"{symbol.value} Funding Rate Cumulative"
    data = []
    for ts, compound, linear in zip(timestamps_coin, cumulative_return_btc, linear_return_coin):
        data.append(
            {
                'date': ts.strftime('%b %y'),
                f'Compound Funding {symbol.value}': round(compound, 2),
                f'Cummulative Funding {symbol.value}': round(linear, 2)
            }
        )
    
    return {"title": title, "data": data}


@app.get("/interest_rates_cumulative")
def get_interest_rates_cumulative(
    stablecoin: Coin = Query(Coin.USDT)
) -> Dict[str, Any]:
    """
    Endpoint to fetch funding rate data for a given symbol.

    Args:
        stablecoin (Coin): The trading symbol (e.g., USDT).

    Returns:
        dict: Contains a title and a list of interest rate records.
    """
    timestamps_stable, interest_rates_stable = read_interest_entries(Coin(stablecoin))

    interest_rates_stable = interest_rates_stable[len(interest_rates_stable) % 8:].reshape(-1, 8).sum(axis=1)
    timestamps_stable = timestamps_stable[len(timestamps_stable) % 8::8]

    compound_interest_stable = 100*(np.cumprod(1 + np.array(interest_rates_stable)) - 1)

    title = f"{stablecoin.value} Interest Rate Cumulative"

    data = []
    for ts, compound in zip(timestamps_stable, compound_interest_stable):
        data.append(
            {
                "date": ts.strftime("%b %y"),
                f"Compound Interest {stablecoin.value}": round(compound, 2)
            }
        )
    
    return {"title": title, "data": data}
