from datetime import datetime, timezone
import numpy as np
import pytest
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from unittest.mock import patch, MagicMock
from backend.models.models_orm import InterestRate, Coin
from backend.data_access.crud.crud_interest import (
    create_interest_entries,
    read_interest_entries,
    read_most_recent_update_interest
)

# Fixtures for mocking the database session
@pytest.fixture
def mock_session():
    with patch("backend.data_access.crud.crud_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session
        yield mock_db_session

# Test that entries are added in bulk with `add_all`
def test_create_interest_entries(mock_session):
    interest_rate_record = InterestRate(coin=Coin.DAI, interest_rate="0.05", interest_rate_timestamp="1700000000000")
    create_interest_entries(interest_rate_record)
    mock_session.merge.assert_called_once_with(interest_rate_record)
    mock_session.commit.assert_called_once()

# Test that rollback is called when IntegrityError occurs
def test_create_interest_entries_integrity_error(mock_session):
    interest_rate_record = InterestRate(coin=Coin.DAI, interest_rate="0.05", interest_rate_timestamp="1700000000000")
    mock_session.commit.side_effect = IntegrityError("mock", "mock", "mock")
    create_interest_entries(interest_rate_record)
    mock_session.rollback.assert_called_once()
    mock_session.commit.assert_called_once()

# Test reading interest rate entries
@pytest.mark.parametrize("num_records, expected_length, expected_timestamps, expected_interest_rates", [
    (2, 2, 
     np.array([datetime(2023, 11, 14, 22, 15, tzinfo=timezone.utc), datetime(2023, 11, 14, 22, 13, 20, tzinfo=timezone.utc)]), 
     np.array([0.05, 0.04])),
    (1, 1, 
     np.array([datetime(2023, 11, 14, 22, 13, 20, tzinfo=timezone.utc)]), 
     np.array([0.05])),
    (0, 0, 
     np.array([]), 
     np.array([]))
])
def test_read_interest_entries(mock_session, num_records, expected_length, expected_timestamps, expected_interest_rates):
    mock_interest_rates = [
        InterestRate(coin=Coin.DAI, interest_rate="0.05", interest_rate_timestamp="1700000000000"),
        InterestRate(coin=Coin.DAI, interest_rate="0.04", interest_rate_timestamp="1700000100000")
    ][:num_records]
    mock_session.query().filter_by().all.return_value = mock_interest_rates
    timestamps, interest_rates_values = read_interest_entries(Coin.DAI)
    np.testing.assert_array_equal(timestamps, expected_timestamps[::-1])
    np.testing.assert_array_equal(interest_rates_values, expected_interest_rates)

# Test if the correct query was executed
def test_read_interest_entries_query_execution(mock_session):
    read_interest_entries(Coin.DAI)
    mock_session.query.assert_called_once_with(InterestRate)
    mock_session.query().filter_by.assert_called_once_with(coin=Coin.DAI.value)
    mock_session.query().filter_by().all.assert_called_once()

# Test that SQLAlchemyError is handled correctly
def test_read_interest_entries_sqlalchemy_error(mock_session):
    mock_session.query.side_effect = SQLAlchemyError("Database error")
    with pytest.raises(SQLAlchemyError):
        read_interest_entries(Coin.DAI)

# Test that unexpected exceptions are handled correctly
def test_read_interest_entries_unexpected_error(mock_session):
    mock_session.query().filter_by().all.side_effect = Exception("Unexpected error")
    with pytest.raises(Exception) as exc_info:
        read_interest_entries(Coin.DAI)
    assert "Unexpected error" in str(exc_info.value)

# Test reading the most recent update interest
@pytest.mark.parametrize("mock_latest_entry, expected_timestamp", [
    (InterestRate(coin=Coin.DAI, interest_rate="0.05", interest_rate_timestamp="1700000000000"), 
     datetime.fromtimestamp(1700000000, tz=timezone.utc)),
    (None, None)
])
def test_read_most_recent_update_interest(mock_session, mock_latest_entry, expected_timestamp):
    mock_session.query().filter_by().order_by().first.return_value = mock_latest_entry
    if mock_latest_entry:
        result = read_most_recent_update_interest(Coin.DAI)
        assert result == expected_timestamp
    else:
        with pytest.raises(AttributeError):
            read_most_recent_update_interest(Coin.DAI)

# Test if the correct query was executed for most recent update
def test_read_most_recent_update_interest_query_execution(mock_session):
    read_most_recent_update_interest(Coin.DAI)
    mock_session.query.assert_called_once_with(InterestRate)
    mock_session.query().filter_by.assert_called_once_with(coin=Coin.DAI.value)
    mock_session.query().filter_by().order_by.assert_called_once()
    mock_session.query().filter_by().order_by().first.assert_called_once()

# Test that SQLAlchemyError is handled correctly in most recent update
def test_read_most_recent_update_interest_sqlalchemy_error(mock_session):
    mock_session.query.side_effect = SQLAlchemyError("Database error")
    with pytest.raises(SQLAlchemyError) as exc_info:
        read_most_recent_update_interest(Coin.DAI)
    assert "Database error" in str(exc_info.value)

# Test that unexpected exceptions are handled correctly in most recent update
def test_read_most_recent_update_interest_unexpected_error(mock_session):
    mock_session.query().filter_by().order_by().first.side_effect = Exception("Unexpected error")
    with pytest.raises(Exception) as exc_info:
        read_most_recent_update_interest(Coin.DAI)
    assert "Unexpected error" in str(exc_info.value)