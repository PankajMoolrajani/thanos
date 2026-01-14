from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Database:
    
    def get_session(self):
        """Create and return a new database session"""
        return self.Session()

# Create a default database instance
db = Database()
