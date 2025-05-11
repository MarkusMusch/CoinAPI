import pytest
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import numpy as np
from backend.models.models_orm import OpenInterest, Symbol
from backend.data_access.crud.crud_open_interest import (
    create_open_interest_entries,
    read_open_interest_entries,
    read_most_recent_update_open_interest
)

# Fixtures for mocking the database session
@pytest.fixture
def mock_session():
    with patch("backend.data_access.crud.crud_open_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session
        yield mock_db_session

# Test that OpenInterest entries are added correctly
def test_create_open_interest_entries(mock_session):
    open_interest_record = OpenInterest(symbol=Symbol.BTCUSDT, open_interest="1000.50", open_interest_timestamp="1700000000000")
    create_open_interest_entries(open_interest_record)
    mock_session.merge.assert_called_once_with(open_interest_record)
    mock_session.commit.assert_called_once()

# Test that rollback is called when IntegrityError occurs
def test_create_open_interest_entries_integrity_error(mock_session):
    open_interest_record = OpenInterest(symbol=Symbol.BTCUSDT, open_interest="1000.50", open_interest_timestamp="1700000000000")
    mock_session.commit.side_effect = IntegrityError("mock", "mock", "mock")
    create_open_interest_entries(open_interest_record)
    mock_session.rollback.assert_called_once()
    mock_session.commit.assert_called_once()

# Test reading open interest entries
@pytest.mark.parametrize("num_records, expected_length, expected_timestamps, expected_open_interest", [
    (2, 2, 
     np.array([datetime(2023, 11, 14, 22, 15, tzinfo=timezone.utc), datetime(2023, 11, 14, 22, 13, 20, tzinfo=timezone.utc)]), 
     np.array([2000.75, 1000.50])),
    (1, 1, 
     np.array([datetime(2023, 11, 14, 22, 13, 20, tzinfo=timezone.utc)]), 
     np.array([1000.50])),
    (0, 0, 
     np.array([]), 
     np.array([]))
])
def test_read_open_interest_entries(mock_session, num_records, expected_length, expected_timestamps, expected_open_interest):
    mock_open_interest = [
        OpenInterest(symbol=Symbol.BTCUSDT, open_interest="1000.50", open_interest_timestamp="1700000000000"),
        OpenInterest(symbol=Symbol.BTCUSDT, open_interest="2000.75", open_interest_timestamp="1700000100000")
    ][:num_records]
    mock_session.query().filter_by().order_by().limit().all.return_value = mock_open_interest
    timestamps, open_interest_values = read_open_interest_entries(Symbol.BTCUSDT, num_values=5)
    np.testing.assert_array_equal(timestamps, expected_timestamps)
    np.testing.assert_array_equal(open_interest_values, expected_open_interest)

# Test if the correct query was executed
def test_read_open_interest_entries_query_execution(mock_session):
    read_open_interest_entries(Symbol.BTCUSDT, num_values=2)
    mock_session.query.assert_called_once_with(OpenInterest)
    mock_session.query().filter_by.assert_called_once_with(symbol=Symbol.BTCUSDT.value)
    mock_session.query().filter_by().order_by.assert_called_once()
    mock_session.query().filter_by().order_by().limit.assert_called_once_with(2)

# Test that SQLAlchemyError is handled correctly
def test_read_open_interest_entries_sqlalchemy_error(mock_session):
    mock_session.query.side_effect = SQLAlchemyError("Database error")
    with pytest.raises(SQLAlchemyError):
        read_open_interest_entries(Symbol.BTCUSDT, num_values=5)

# Test that unexpected exceptions are handled correctly
def test_read_open_interest_entries_unexpected_error(mock_session):
    mock_session.query().filter_by().order_by().limit().all.side_effect = Exception("Unexpected error")
    with pytest.raises(Exception) as exc_info:
        read_open_interest_entries(Symbol.BTCUSDT, num_values=5)
    assert "Unexpected error" in str(exc_info.value)

# Test reading the most recent update open interest
@pytest.mark.parametrize("mock_latest_entry, expected_timestamp", [
    (OpenInterest(symbol=Symbol.BTCUSDT, open_interest="1000.50", open_interest_timestamp="1700000000000"), 
     datetime.fromtimestamp(1700000000, tz=timezone.utc)),
    (None, None)
])
def test_read_most_recent_update_open_interest(mock_session, mock_latest_entry, expected_timestamp):
    mock_session.query().filter_by().order_by().first.return_value = mock_latest_entry
    if mock_latest_entry:
        result = read_most_recent_update_open_interest(Symbol.BTCUSDT)
        assert result == expected_timestamp
    else:
        with pytest.raises(AttributeError):
            read_most_recent_update_open_interest(Symbol.BTCUSDT)

# Test if the correct query was executed for most recent update
def test_read_most_recent_update_open_interest_query_execution(mock_session):
    read_most_recent_update_open_interest(Symbol.BTCUSDT)
    mock_session.query.assert_called_once_with(OpenInterest)
    mock_session.query().filter_by.assert_called_once_with(symbol=Symbol.BTCUSDT.value)
    mock_session.query().filter_by().order_by.assert_called_once()
    mock_session.query().filter_by().order_by().first.assert_called_once()

# Test that SQLAlchemyError is handled correctly in most recent update
def test_read_most_recent_update_open_interest_sqlalchemy_error(mock_session):
    mock_session.query.side_effect = SQLAlchemyError("Database error")
    with pytest.raises(SQLAlchemyError) as exc_info:
        read_most_recent_update_open_interest(Symbol.BTCUSDT)
    assert "Database error" in str(exc_info.value)

# Test that unexpected exceptions are handled correctly in most recent update
def test_read_most_recent_update_open_interest_unexpected_error(mock_session):
    mock_session.query().filter_by().order_by().first.side_effect = Exception("Unexpected error")
    with pytest.raises(Exception) as exc_info:
        read_most_recent_update_open_interest(Symbol.BTCUSDT)
    assert "Unexpected error" in str(exc_info.value)