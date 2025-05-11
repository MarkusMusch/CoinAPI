from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from backend.models.models_orm import Coin, FundingRate, InterestRate, OpenInterest, Symbol


class TestFundingRateORMModel:

    def test_funding_rate_insert(self, session):
        # Create a test FundingRate object
        symbol = Symbol.BTCUSDT
        funding_rate = "0.05"
        funding_rate_timestamp = "1700000000000"  # Test timestamp

        # Insert the FundingRate object into the database
        funding_rate_obj = FundingRate(symbol=symbol, funding_rate=funding_rate, funding_rate_timestamp=funding_rate_timestamp)
        session.add(funding_rate_obj)
        session.commit()

        # Query the object back from the database
        queried_obj = session.query(FundingRate).filter_by(symbol=symbol).first()

        # Check if the inserted object matches the expected values
        assert queried_obj is not None
        assert queried_obj.symbol == symbol
        assert queried_obj.funding_rate == 0.05  # Converted from string
        expected_datetime = datetime(2023, 11, 14, 22, 13, 20)
        assert queried_obj.funding_rate_timestamp ==  expected_datetime


    def test_funding_rate_null_constraints(self, session):
        symbol = None  # Null value for non-nullable field
        funding_rate = "0.05"
        funding_rate_timestamp = "1700000000000"

        with pytest.raises(IntegrityError):
            funding_rate_obj = FundingRate(symbol=symbol, funding_rate=funding_rate, funding_rate_timestamp=funding_rate_timestamp)
            session.add(funding_rate_obj)
            session.commit()


    def test_funding_rate_primary_key_uniqueness(self, session):
        symbol = Symbol.BTCUSDT
        funding_rate = "0.05"
        funding_rate_timestamp = "1700000000000"

        # Insert the first FundingRate object
        funding_rate_obj1 = FundingRate(symbol=symbol, funding_rate=funding_rate, funding_rate_timestamp=funding_rate_timestamp)
        session.add(funding_rate_obj1)
        session.commit()

        # Attempt to insert a duplicate FundingRate object
        with pytest.raises(IntegrityError):
            funding_rate_obj2 = FundingRate(symbol=symbol, funding_rate=funding_rate, funding_rate_timestamp=funding_rate_timestamp)
            session.add(funding_rate_obj2)
            session.commit()

    def test_funding_rate_multiple_symbols(self, session):
        funding_rate1 = "0.05"
        funding_rate2 = "0.07"
        funding_rate_timestamp1 = "1700000000000"
        funding_rate_timestamp2 = "1700000100000"

        # Insert two FundingRate objects with different symbols
        funding_rate_obj1 = FundingRate(symbol=Symbol.BTCUSDT, funding_rate=funding_rate1, funding_rate_timestamp=funding_rate_timestamp1)
        funding_rate_obj2 = FundingRate(symbol=Symbol.ETHUSDT, funding_rate=funding_rate2, funding_rate_timestamp=funding_rate_timestamp2)

        session.add(funding_rate_obj1)
        session.add(funding_rate_obj2)
        session.commit()

        # Query both objects and check they were inserted correctly
        queried_btc = session.query(FundingRate).filter_by(symbol=Symbol.BTCUSDT).first()
        queried_eth = session.query(FundingRate).filter_by(symbol=Symbol.ETHUSDT).first()

        assert queried_btc.funding_rate == 0.05
        assert queried_eth.funding_rate == 0.07

    def test_funding_rate_float_conversion(self, session):
        symbol = Symbol.BTCUSDT
        funding_rate = "0.05"
        funding_rate_timestamp = "1700000000000"

        # Insert the FundingRate object
        funding_rate_obj = FundingRate(symbol=symbol, funding_rate=funding_rate, funding_rate_timestamp=funding_rate_timestamp)
        session.add(funding_rate_obj)
        session.commit()

        # Query the object back from the database
        queried_obj = session.query(FundingRate).filter_by(symbol=symbol).first()

        # Ensure the funding_rate was properly converted to float
        assert isinstance(queried_obj.funding_rate, float)
        assert queried_obj.funding_rate == 0.05

    def test_funding_rate_timestamp_conversion(self, session):
        symbol = Symbol.BTCUSDT
        funding_rate = "0.05"
        funding_rate_timestamp = "1700000000000"  # Milliseconds timestamp

        # Insert the FundingRate object
        funding_rate_obj = FundingRate(symbol=symbol, funding_rate=funding_rate, funding_rate_timestamp=funding_rate_timestamp)
        session.add(funding_rate_obj)
        session.commit()

        # Query the object back from the database
        queried_obj = session.query(FundingRate).filter_by(symbol=symbol).first()

        # Verify the timestamp was correctly converted to a datetime object
        expected_datetime = datetime(2023, 11, 14, 22, 13, 20)
        assert queried_obj.funding_rate_timestamp == expected_datetime

    def test_funding_rate_invalid_float_conversion(self):
        symbol = Symbol.BTCUSDT
        funding_rate = "invalid_rate"  # Invalid string that cannot be converted to float
        funding_rate_timestamp = "1700000000000"

        with pytest.raises(ValueError):
            funding_rate_obj = FundingRate(symbol=symbol, funding_rate=funding_rate, funding_rate_timestamp=funding_rate_timestamp)
    
    def test_funding_rate_empty_string(self):
        symbol = Symbol.BTCUSDT
        funding_rate = ""  # Empty string
        funding_rate_timestamp = "1700000000000"

        with pytest.raises(ValueError):
            funding_rate_obj = FundingRate(symbol=symbol, funding_rate=funding_rate, funding_rate_timestamp=funding_rate_timestamp)


class TestOpenInterestORMModel:

    def test_open_interest_insert(self, session):
        # Create a test OpenInterest object
        symbol = Symbol.BTCUSDT
        open_interest = "5000.25"
        open_interest_timestamp = "1700000000000"  # Test timestamp

        # Insert the OpenInterest object into the database
        open_interest_obj = OpenInterest(symbol=symbol, open_interest=open_interest, open_interest_timestamp=open_interest_timestamp)
        session.add(open_interest_obj)
        session.commit()

        # Query the object back from the database
        queried_obj = session.query(OpenInterest).filter_by(symbol=symbol).first()

        # Check if the inserted object matches the expected values
        assert queried_obj is not None
        assert queried_obj.symbol == symbol
        assert queried_obj.open_interest == 5000.25  # Converted from string
        expected_datetime = datetime(2023, 11, 14, 22, 13, 20)
        assert queried_obj.open_interest_timestamp == expected_datetime

    def test_open_interest_null_constraints(self, session):
        symbol = None  # Null value for non-nullable field
        open_interest = "5000.25"
        open_interest_timestamp = "1700000000000"

        with pytest.raises(IntegrityError):
            open_interest_obj = OpenInterest(symbol=symbol, open_interest=open_interest, open_interest_timestamp=open_interest_timestamp)
            session.add(open_interest_obj)
            session.commit()

    def test_open_interest_primary_key_uniqueness(self, session):
        symbol = Symbol.BTCUSDT
        open_interest = "5000.25"
        open_interest_timestamp = "1700000000000"

        # Insert the first OpenInterest object
        open_interest_obj1 = OpenInterest(symbol=symbol, open_interest=open_interest, open_interest_timestamp=open_interest_timestamp)
        session.add(open_interest_obj1)
        session.commit()

        # Attempt to insert a duplicate OpenInterest object
        with pytest.raises(IntegrityError):
            open_interest_obj2 = OpenInterest(symbol=symbol, open_interest=open_interest, open_interest_timestamp=open_interest_timestamp)
            session.add(open_interest_obj2)
            session.commit()

    def test_open_interest_multiple_symbols(self, session):
        open_interest1 = "5000.25"
        open_interest2 = "6000.75"
        open_interest_timestamp1 = "1700000000000"
        open_interest_timestamp2 = "1700000100000"

        # Insert two OpenInterest objects with different symbols
        open_interest_obj1 = OpenInterest(symbol=Symbol.BTCUSDT, open_interest=open_interest1, open_interest_timestamp=open_interest_timestamp1)
        open_interest_obj2 = OpenInterest(symbol=Symbol.ETHUSDT, open_interest=open_interest2, open_interest_timestamp=open_interest_timestamp2)

        session.add(open_interest_obj1)
        session.add(open_interest_obj2)
        session.commit()

        # Query both objects and check they were inserted correctly
        queried_btc = session.query(OpenInterest).filter_by(symbol=Symbol.BTCUSDT).first()
        queried_eth = session.query(OpenInterest).filter_by(symbol=Symbol.ETHUSDT).first()

        assert queried_btc.open_interest == 5000.25
        assert queried_eth.open_interest == 6000.75

    def test_open_interest_float_conversion(self, session):
        symbol = Symbol.BTCUSDT
        open_interest = "5000.25"
        open_interest_timestamp = "1700000000000"

        # Insert the OpenInterest object
        open_interest_obj = OpenInterest(symbol=symbol, open_interest=open_interest, open_interest_timestamp=open_interest_timestamp)
        session.add(open_interest_obj)
        session.commit()

        # Query the object back from the database
        queried_obj = session.query(OpenInterest).filter_by(symbol=symbol).first()

        # Ensure the open_interest was properly converted to float
        assert isinstance(queried_obj.open_interest, float)
        assert queried_obj.open_interest == 5000.25

    def test_open_interest_timestamp_conversion(self, session):
        symbol = Symbol.BTCUSDT
        open_interest = "5000.25"
        open_interest_timestamp = "1700000000000"  # Milliseconds timestamp

        # Insert the OpenInterest object
        open_interest_obj = OpenInterest(symbol=symbol, open_interest=open_interest, open_interest_timestamp=open_interest_timestamp)
        session.add(open_interest_obj)
        session.commit()

        # Query the object back from the database
        queried_obj = session.query(OpenInterest).filter_by(symbol=symbol).first()

        # Verify the timestamp was correctly converted to a datetime object
        expected_datetime = datetime(2023, 11, 14, 22, 13, 20)
        assert queried_obj.open_interest_timestamp == expected_datetime

    def test_open_interest_invalid_float_conversion(self):
        symbol = Symbol.BTCUSDT
        open_interest = "invalid_open_interest"  # Invalid string that cannot be converted to float
        open_interest_timestamp = "1700000000000"

        with pytest.raises(ValueError):
            open_interest_obj = OpenInterest(symbol=symbol, open_interest=open_interest, open_interest_timestamp=open_interest_timestamp)
    
    def test_open_interest_empty_string(self):
        symbol = Symbol.BTCUSDT
        open_interest = ""  # Empty string
        open_interest_timestamp = "1700000000000"

        with pytest.raises(ValueError):
            open_interest_obj = OpenInterest(symbol=symbol, open_interest=open_interest, open_interest_timestamp=open_interest_timestamp)


class TestInterestRateORMModel:

    def test_interest_rate_insert(self, session):
        # Create a test InterestRate object
        coin = Coin.DAI
        interest_rate = "0.02"
        interest_rate_timestamp = "1700000000000"

        # Insert the InterestRate object into the database
        interest_rate_obj = InterestRate(coin=coin, interest_rate=interest_rate, interest_rate_timestamp=interest_rate_timestamp)
        session.add(interest_rate_obj)
        session.commit()

        # Query the object back from the database
        queried_obj = session.query(InterestRate).filter_by(coin=coin).first()

        # Check if the inserted object matches the expected values
        assert queried_obj is not None
        assert queried_obj.coin == coin
        assert queried_obj.interest_rate == 0.02  # Converted from string
        expected_datetime = datetime(2023, 11, 14, 22, 13, 20)
        assert queried_obj.interest_rate_timestamp == expected_datetime

    def test_interest_rate_null_constraints(self, session):
        coin = None  # Null value for non-nullable field
        interest_rate = "0.02"
        interest_rate_timestamp = "1700000000000"

        with pytest.raises(IntegrityError):
            interest_rate_obj = InterestRate(coin=coin, interest_rate=interest_rate, interest_rate_timestamp=interest_rate_timestamp)
            session.add(interest_rate_obj)
            session.commit()

    def test_interest_rate_primary_key_uniqueness(self, session):
        coin = Coin.DAI
        interest_rate = "0.02"
        interest_rate_timestamp = "1700000000000"

        # Insert the first InterestRate object
        interest_rate_obj1 = InterestRate(coin=coin, interest_rate=interest_rate, interest_rate_timestamp=interest_rate_timestamp)
        session.add(interest_rate_obj1)
        session.commit()

        # Attempt to insert a duplicate InterestRate object
        with pytest.raises(IntegrityError):
            interest_rate_obj2 = InterestRate(coin=coin, interest_rate=interest_rate, interest_rate_timestamp=interest_rate_timestamp)
            session.add(interest_rate_obj2)
            session.commit()

    def test_interest_rate_float_conversion(self, session):
        coin = Coin.DAI
        interest_rate = "0.02"
        interest_rate_timestamp = "1700000000000"

        # Insert the InterestRate object
        interest_rate_obj = InterestRate(coin=coin, interest_rate=interest_rate, interest_rate_timestamp=interest_rate_timestamp)
        session.add(interest_rate_obj)
        session.commit()

        # Query the object back from the database
        queried_obj = session.query(InterestRate).filter_by(coin=coin).first()

        # Ensure the interest_rate was properly converted to float
        assert isinstance(queried_obj.interest_rate, float)
        assert queried_obj.interest_rate == 0.02

    def test_interest_rate_timestamp_conversion(self, session):
        coin = Coin.DAI
        interest_rate = "0.02"
        interest_rate_timestamp = "1700000000000"

        # Insert the InterestRate object
        interest_rate_obj = InterestRate(coin=coin, interest_rate=interest_rate, interest_rate_timestamp=interest_rate_timestamp)
        session.add(interest_rate_obj)
        session.commit()

        # Query the object back from the database
        queried_obj = session.query(InterestRate).filter_by(coin=coin).first()

        # Verify the timestamp was correctly converted to a datetime object
        expected_datetime = datetime(2023, 11, 14, 22, 13, 20)
        assert queried_obj.interest_rate_timestamp == expected_datetime

    def test_interest_rate_invalid_float_conversion(self):
        coin = Coin.DAI
        interest_rate = "invalid_rate"  # Invalid string that cannot be converted to float
        interest_rate_timestamp = "1700000000000"

        with pytest.raises(ValueError):
            interest_rate_obj = InterestRate(coin=coin, interest_rate=interest_rate, interest_rate_timestamp=interest_rate_timestamp)

    def test_interest_rate_empty_string(self):
        coin = Coin.DAI
        interest_rate = ""
        interest_rate_timestamp = "1700000000000"

        with pytest.raises(ValueError):
            interest_rate_obj = InterestRate(coin=coin, interest_rate=interest_rate, interest_rate_timestamp=interest_rate_timestamp)