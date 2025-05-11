""" This module contains CRUD functions for the funding rate data. """
from typing import Optional, Tuple, Union

import numpy as np
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
import logging

from backend.config import Session
from backend.models.models_orm import FundingRate, Symbol

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_funding_entries(funding_rate_record: FundingRate) -> None:
    """Create a new funding rate record in the database.
    
    Args:
        funding_rate_record (FundingRate): The funding rate record to be added.
    """
    with Session() as session:
        try:
            session.merge(funding_rate_record)
            session.commit()
            logger.info("Funding rate record added successfully: %s", funding_rate_record)
        except Exception as e:
            logger.error("An error occurred while adding funding rate record: %s", e)
            session.rollback()


def read_funding_entries(symbol: Symbol, num_values: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    """Read funding rate records from the database.

    Args:
        symbol (Symbol): The symbol for which the funding rate records should be read.
        num_values (int, optional): The number of funding rate records to be read. If None, all records are read. Defaults to None.

    Returns:
        tuple: A tuple containing the timestamps and funding rate values.
    """
    try:
        with Session() as session:
            funding_rates = (
                session.query(FundingRate)
                    .filter_by(symbol=symbol.value)
                    .order_by(desc(FundingRate.funding_rate_timestamp))
                    .limit(num_values)
                    .all()
            )
            logger.info("Funding rate records fetched successfully for symbol %s", symbol.value)
        
        timestamps = np.array([entry.funding_rate_timestamp for entry in funding_rates])[::-1]
        funding_rate_values = np.array([entry.funding_rate for entry in funding_rates])[::-1]
        return timestamps, funding_rate_values
    except SQLAlchemyError as e:
        logger.error("Database error occurred while reading Funding Rate data: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while reading Funding Rate data: %s", e)
        raise


def read_most_recent_update_funding(symbol: Symbol) -> Union[str, None]:
    """Read the date of the most recent funding rate update from the database.

    Args:
        symbol (Symbol): The symbol for which the most recent funding rate update should be read.

    Returns:
        str: The timestamp of the most recent funding rate update.
    """
    try:
        with Session() as session:
            latest_entry = (
                session.query(FundingRate)
                    .filter_by(symbol=symbol.value)
                    .order_by(desc(FundingRate.funding_rate_timestamp))
                    .first()
            )

        if latest_entry is None:
            logger.info("No funding rate data found for coin %s", symbol.value)
            return None
            
        date_time = latest_entry.funding_rate_timestamp
        logger.info("Most recent funding rate update for symbol %s: %s", symbol.value, date_time)
        return date_time
    except SQLAlchemyError as e:
        logger.error("Database error occurred while reading the most recent Funding Rate data timestamp: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while reading the most recent Funding Rate data timestamp: %s", e)
        raise