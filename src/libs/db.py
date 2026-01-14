import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self, db_url=None):
        # Use environment variable or default to local SQLite
        if db_url is None:
            db_url = os.getenv('DATABASE_URL', 'sqlite:///thanos.db')
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        """Create and return a new database session"""
        return self.Session()

# Create a default database instance
db = Database()
