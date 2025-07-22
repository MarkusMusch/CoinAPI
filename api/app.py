from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from sqlalchemy import create_engine
from typing import Any, Dict, Optional

from data_layer.data_access.api_client.bybit_client import ByBitClient
from data_layer.data_access.crud.crud_funding import (
    read_funding_entries,
    read_most_recent_update_funding
)
from data_layer.data_access.crud.crud_interest import (
    read_interest_entries,
    read_most_recent_update_interest
)
from data_layer.data_access.crud.crud_open_interest import read_most_recent_update_open_interest
from data_layer.models.models_api import ChartData
from data_layer.models.models_orm import Base, Coin, Symbol
from data_layer.services.download_data import (
    catch_latest_funding,
    catch_latest_open_interest,
    catch_latest_interest,
    fill_funding,
    fill_interest,
    fill_open_interest
)


engine = create_engine('sqlite:///funding_history.db')
Base.metadata.create_all(engine)


client = ByBitClient()

for symbol in Symbol:

    most_recent_funding = read_most_recent_update_funding(symbol)

    if most_recent_funding is not None:
        catch_latest_funding(
            client,
            symbol,
            most_recent_funding
        )
    else:
        fill_funding(
            client,
            symbol
        )
    
    most_recent_oi = read_most_recent_update_open_interest(symbol)

    if most_recent_oi is not None:
        catch_latest_open_interest(
            client,
            symbol,
            most_recent_oi
        )
    else:
        fill_open_interest(
            client,
            symbol
        )
"""
for coin in Coin:

    most_recent_datetime = read_most_recent_update_interest(coin)
    
    if most_recent_datetime is not None:
        catch_latest_interest(
            client,
            coin,
            most_recent_datetime
        )
    else:
        fill_interest(
            client,
            coin
        )
"""

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/chart")
def read_chart():
    response = ChartData(
        data=[
            { "date": '2025-03-01', "Apples": 400, "Oranges": 300 },
            { "date": '2025-03-02', "Apples": 300, "Oranges": 500 },
            { "date": '2025-03-03', "Apples": 450, "Oranges": 350 },
            { "date": '2025-03-04', "Apples": 500, "Oranges": 400 }
        ],
        dataKey="date",
        series=[
            { "name": 'Apples', "color": '#1E90FF' },
            { "name": 'Oranges', "color": '#FFA500' },
        ]
    )
    return response
