from datetime import datetime, timezone
import numpy as np
import pytest
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from unittest.mock import patch, MagicMock
from backend.models.models_orm import FundingRate, Symbol
from backend.data_access.crud.crud_funding import (
    create_funding_entries,
    read_funding_entries,
    read_most_recent_update_funding
)

# Fixtures for mocking the database session
@pytest.fixture
def mock_session():
    with patch("backend.data_access.crud.crud_funding.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session
        yield mock_db_session

# Test that entries are added in bulk with `add_all`
def test_create_funding_entries(mock_session):
    funding_rate_record = FundingRate(symbol=Symbol.BTCUSDT, funding_rate="0.01", funding_rate_timestamp="1700000000000")
    create_funding_entries(funding_rate_record)
    mock_session.merge.assert_called_once_with(funding_rate_record)
    mock_session.commit.assert_called_once()

# Test that rollback is called when IntegrityError occurs
def test_create_funding_entries_integrity_error(mock_session):
    funding_rate_record = FundingRate(symbol=Symbol.BTCUSDT, funding_rate="0.01", funding_rate_timestamp="1700000000000")
    mock_session.commit.side_effect = IntegrityError("mock", "mock", "mock")
    create_funding_entries(funding_rate_record)
    mock_session.rollback.assert_called_once()
    mock_session.commit.assert_called_once()

# Test reading funding entries
@pytest.mark.parametrize("num_records, expected_length, expected_timestamps, expected_funding_rates", [
    (2, 2, 
     np.array([datetime(2023, 11, 14, 22, 15, tzinfo=timezone.utc), datetime(2023, 11, 14, 22, 13, 20, tzinfo=timezone.utc)]), 
     np.array([0.01, 0.02])),
    (1, 1, 
     np.array([datetime(2023, 11, 14, 22, 13, 20, tzinfo=timezone.utc)]), 
     np.array([0.01])),
    (0, 0, 
     np.array([]), 
     np.array([]))
])
def test_read_funding_entries(mock_session, num_records, expected_length, expected_timestamps, expected_funding_rates):
    mock_funding_rates = [
        FundingRate(symbol=Symbol.BTCUSDT, funding_rate="0.01", funding_rate_timestamp="1700000000000"),
        FundingRate(symbol=Symbol.BTCUSDT, funding_rate="0.02", funding_rate_timestamp="1700000100000")
    ][:num_records]
    mock_session.query().filter_by().order_by().limit().all.return_value = mock_funding_rates
    timestamps, funding_rates_values = read_funding_entries(Symbol.BTCUSDT, num_values=5)
    np.testing.assert_array_equal(timestamps, expected_timestamps)
    np.testing.assert_array_equal(funding_rates_values, expected_funding_rates[::-1])

# Test if the correct query was executed
def test_read_funding_entries_query_execution(mock_session):
    read_funding_entries(Symbol.BTCUSDT, num_values=2)
    mock_session.query.assert_called_once_with(FundingRate)
    mock_session.query().filter_by.assert_called_once_with(symbol=Symbol.BTCUSDT.value)
    mock_session.query().filter_by().order_by.assert_called_once()
    mock_session.query().filter_by().order_by().limit.assert_called_once_with(2)

# Test that SQLAlchemyError is handled correctly
def test_read_funding_entries_sqlalchemy_error(mock_session):
    mock_session.query.side_effect = SQLAlchemyError("Database error")
    with pytest.raises(SQLAlchemyError):
        read_funding_entries(Symbol.BTCUSDT, num_values=5)

# Test that unexpected exceptions are handled correctly
def test_read_funding_entries_unexpected_error(mock_session):
    mock_session.query().filter_by().order_by().limit().all.side_effect = Exception("Unexpected error")
    with pytest.raises(Exception) as exc_info:
        read_funding_entries(Symbol.BTCUSDT, num_values=5)
    assert "Unexpected error" in str(exc_info.value)

# Test reading the most recent update funding
@pytest.mark.parametrize("mock_latest_entry, expected_timestamp", [
    (FundingRate(symbol=Symbol.BTCUSDT, funding_rate="0.01", funding_rate_timestamp="1700000000000"), 
     datetime.fromtimestamp(1700000000, tz=timezone.utc)),
    (None, None)
])
def test_read_most_recent_update_funding(mock_session, mock_latest_entry, expected_timestamp):
    mock_session.query().filter_by().order_by().first.return_value = mock_latest_entry
    if mock_latest_entry:
        result = read_most_recent_update_funding(Symbol.BTCUSDT)
        assert result == expected_timestamp
    else:
        with pytest.raises(AttributeError):
            read_most_recent_update_funding(Symbol.BTCUSDT)

# Test if the correct query was executed for most recent update
def test_read_most_recent_update_funding_query_execution(mock_session):
    read_most_recent_update_funding(Symbol.BTCUSDT)
    mock_session.query.assert_called_once_with(FundingRate)
    mock_session.query().filter_by.assert_called_once_with(symbol=Symbol.BTCUSDT.value)
    mock_session.query().filter_by().order_by.assert_called_once()
    mock_session.query().filter_by().order_by().first.assert_called_once()

# Test that SQLAlchemyError is handled correctly in most recent update
def test_read_most_recent_update_funding_sqlalchemy_error(mock_session):
    mock_session.query.side_effect = SQLAlchemyError("Database error")
    with pytest.raises(SQLAlchemyError) as exc_info:
        read_most_recent_update_funding(Symbol.BTCUSDT)
    assert "Database error" in str(exc_info.value)

# Test that unexpected exceptions are handled correctly in most recent update
def test_read_most_recent_update_funding_unexpected_error(mock_session):
    mock_session.query().filter_by().order_by().first.side_effect = Exception("Unexpected error")
    with pytest.raises(Exception) as exc_info:
        read_most_recent_update_funding(Symbol.BTCUSDT)
    assert "Unexpected error" in str(exc_info.value)