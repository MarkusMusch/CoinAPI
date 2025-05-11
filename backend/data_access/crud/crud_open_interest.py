""" This module contains CRUD functions for the OpenInterest table. """
from typing import Optional, Tuple, Union

import numpy as np
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
import logging

from backend.config import Session
from backend.models.models_orm import OpenInterest, Symbol

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_open_interest_entries(open_interest_record: OpenInterest) -> None:
    """Create a new open interest record in the database.

    Args:
        open_interest_record (OpenInterest): The open interest record to be added.
    """
    with Session() as session:
        try:
            session.merge(open_interest_record)
            session.commit()
            logger.info("Open interest record added successfully: %s", open_interest_record)
        except Exception as e:
            logger.error("An error occurred while adding open interest record: %s", e)
            session.rollback()


def read_open_interest_entries(symbol: Symbol, num_values: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    """Read open interest records from the database.

    Args:
        symbol (Symbol): The symbol for which the open interest records should be read.
        num_values (int, optional): The number of open interest records to be read. If None, all records are read. Defaults to None.

    Returns:
        tuple: A tuple containing the timestamps and open interest values.
    """
    try:
        with Session() as session:
            open_interest = (
                session.query(OpenInterest)
                    .filter_by(symbol=symbol.value)
                    .order_by(desc(OpenInterest.open_interest_timestamp))
                    .limit(num_values)
                    .all()
            )
            logger.info("Open interest records fetched successfully for symbol %s", symbol.value)

        timestamps = np.array([rate.open_interest_timestamp for rate in open_interest])[::-1]
        open_interest_values = np.array([float(rate.open_interest) for rate in open_interest])[::-1]
        
        return timestamps, open_interest_values
    except SQLAlchemyError as e:
        logger.error("Database error occurred while reading Open Interest data: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error occurred while reading Open Interest data: %s", e)
        raise


def read_most_recent_update_open_interest(symbol: Symbol) -> Union[str, None]:
    """Read the date of the most recent open interest update from the database.

    Args:
        symbol (Symbol): The symbol for which the most recent open interest update should be read.

    Returns:
        str: The timestamp of the most recent open interest update.
    """
    try:
        with Session() as session:
            latest_entry = (
                session.query(OpenInterest)
                    .filter_by(symbol=symbol.value)
                    .order_by(desc(OpenInterest.open_interest_timestamp))
                    .first()
            )

        if latest_entry is None:
            logger.info("No open interest data found for coin %s", symbol.value)
            return None
            
        date_time = latest_entry.open_interest_timestamp
        logger.info("Most recent open interest update for symbol %s: %s", symbol.value, date_time)
        return date_time
    except SQLAlchemyError as e:
        logger.error("Database error occurred while reading the most recent Open Interest data timestamp: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error occurred while reading the most recent Open Interest data timestamp: %s", e)
        raise