from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Database configuration
DATABASE_URL = 'sqlite:///funding_history.db'


# Create engine
engine = create_engine(DATABASE_URL)


# Create a session factory
Session = scoped_session(sessionmaker(bind=engine))