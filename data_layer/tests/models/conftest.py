import warnings

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import SAWarning
from sqlalchemy.orm import sessionmaker

from backend.models.models_orm import Base


# Fixture to set up the test database and session
@pytest.fixture(scope="function")
def session():
    # Suppress the specific SAWarning
    warnings.filterwarnings("ignore", category=SAWarning)

    # Create an in-memory SQLite database for testing
    engine = create_engine('sqlite:///:memory:')
    
    # Create all the tables in the test database
    Base.metadata.create_all(engine)
    
    # Create a new session for interacting with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session  # Provide the session to the test

    session.close()  # Close the session after the test