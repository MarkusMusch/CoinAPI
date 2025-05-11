""" ORM models for the database. """
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Column, DateTime, Enum as SQLEnum, Float
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Symbol(str, Enum):
    """Enum for the trading symbols."""
    BTCUSDT = 'BTCUSDT'
    BTCUSDC = 'BTCPERP'
    BTCUSD = 'BTCUSD'
    ETHUSDT = 'ETHUSDT'
    ETHUSDC = 'ETHPERP'
    ETHUSD = 'ETHUSD'
    SOLUSDT = 'SOLUSDT'
    SOLUSDC = 'SOLPERP'
    SOLUSD = 'SOLUSD'
    SUIUSDT = 'SUIUSDT'
    SUIUSDC = 'SUIPERP'
    USDCUSDT = 'USDCUSDT'
    USDEUSDT = 'USDEUSDT'
    XRPUSDT = 'XRPUSDT'
    XRPUSD = 'XRPUSD'
    BNBUSDT = 'BNBUSDT'
    DOGEUSDT = 'DOGEUSDT'
    ADAUSDT = 'ADAUSDT'
    ADAUSD = 'ADAUSD'
    BONKUSDT = '1000BONKUSDT'
    WIFUSDT = 'WIFUSDT'
    CHILLGUYUSDT = 'CHILLGUYUSDT'
    PEPEUSDT = '1000PEPEUSDT'
    TOSHIUSDT = '1000TOSHIUSDT'
    GIGAUSDT = 'GIGAUSDT'
    GOATUSDT = 'GOATUSDT'
    RENDERUSDT = 'RENDERUSDT'
    AKTUSDT = 'AKTUSDT'
    SHIBUSDT = 'SHIB1000USDT'
    POPCATUSDT = 'POPCATUSDT'
    BRETTUSDT = 'BRETTUSDT'
    MOGUSDT = '1000000MOGUSDT'
    MOODENGUSDT = 'MOODENGUSDT'
    APUSUDT = '1000APUUSDT'
    ETHBTCUSDT = 'ETHBTCUSDT'


class Coin(str, Enum):
    """Enum for the coins."""
    DAI = 'DAI'
    USDT = 'USDT'
    USDC = 'USDC'
    USDE = 'USDE'
    TUSD = 'TUSD'


class FundingRate(Base):
    """ORM model for the funding rates."""
    __tablename__ = 'funding_rates'

    symbol = Column(SQLEnum(Symbol), primary_key=True, nullable=False)
    funding_rate_timestamp = Column(DateTime, primary_key=True, nullable=False)
    funding_rate = Column(Float, nullable=False)

    def __init__(self, symbol: Symbol, funding_rate: str, funding_rate_timestamp: str) -> None:
        self.symbol = symbol
        self.funding_rate = float(funding_rate)
        self.funding_rate_timestamp = datetime.fromtimestamp(int(funding_rate_timestamp) / 1000, tz=timezone.utc)


class OpenInterest(Base):
    """ORM model for the open interest."""
    __tablename__ = 'open_interest'

    symbol = Column(SQLEnum(Symbol), primary_key=True, nullable=False)
    open_interest_timestamp = Column(DateTime, primary_key=True, nullable=False)
    open_interest = Column(Float, nullable=False)

    def __init__(self, symbol: Symbol, open_interest: str, open_interest_timestamp: str) -> None:
        self.symbol = symbol
        self.open_interest = float(open_interest)
        self.open_interest_timestamp = datetime.fromtimestamp(int(open_interest_timestamp) / 1000, tz=timezone.utc)


class InterestRate(Base):
    """ORM model for the interest rates."""
    __tablename__ = 'interest_rates'

    coin = Column(SQLEnum(Coin), primary_key=True, nullable=False)
    interest_rate_timestamp = Column(DateTime, primary_key=True, nullable=False)
    interest_rate = Column(Float, nullable=False)

    def __init__(self, coin: Coin, interest_rate: str, interest_rate_timestamp: str) -> None:
        self.coin = coin 
        self.interest_rate = float(interest_rate)
        self.interest_rate_timestamp = datetime.fromtimestamp(int(interest_rate_timestamp) / 1000, tz=timezone.utc)