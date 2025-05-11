""" This module contains the CRUD operations for the InterestRate model. """
import logging
from typing import Tuple, Union

import numpy as np
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from backend.config import Session
from backend.models.models_orm import Coin, InterestRate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_interest_entries(interest_rate_record: InterestRate) -> None:
    """Create a new interest rate record in the database.

    Args:
        interest_rate_record (InterestRate): The interest rate record to be added.
    """
    with Session() as session:
        try:
            session.merge(interest_rate_record)
            session.commit()
            logger.info("Interest rate record added successfully: %s", interest_rate_record)
        except Exception as e:
            logger.error("An error occurred while adding interest rate record: %s", e)
            session.rollback()


def read_interest_entries(coin: Coin) -> Tuple[np.ndarray, np.ndarray]:
    """Read interest rate records from the database.
    
    Args:
        coin (Coin): The coin for which the interest rate records should be read.
        
    Returns:
        tuple: A tuple containing the timestamps and interest rate values.
    """
    try:
        with Session() as session:
            interest_rates = session.query(InterestRate).filter_by(coin=coin.value).all()
            logger.info("Interest rate records fetched successfully for coin %s", coin.value)

        timestamps = np.array([rate.interest_rate_timestamp for rate in interest_rates])
        interest_rates_values = np.array([float(rate.interest_rate) for rate in interest_rates])
        
        return timestamps, interest_rates_values
    except SQLAlchemyError as e:
        logger.error("Database error occurred while reading Interest Rate data: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while reading Interest Rate data: %s", e)
        raise


def read_most_recent_update_interest(coin: Coin) -> Union[str, None]:
    """Read the date of the most recent interest rate update from the database.

    Args:
        coin (Coin): The coin for which the most recent interest rate update should be read.

    Returns:
        str: The timestamp of the most recent interest rate update.
    """
    try:
        with Session() as session:
            latest_entry = (
                session.query(InterestRate)
                    .filter_by(coin=coin.value)
                    .order_by(desc(InterestRate.interest_rate_timestamp))
                    .first()
            )

        if latest_entry is None:
            logger.info("No interest rate data found for coin %s", coin.value)
            return None
         
        date_time = latest_entry.interest_rate_timestamp
        logger.info("Most recent interest rate update for coin %s: %s", coin.value, date_time)
        return date_time
    except SQLAlchemyError as e:
        logger.error("Database error occurred while reading the most recent Interest Rate data timestamp: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while reading the most recent Interest Rate data timestamp: %s", e)
        raise