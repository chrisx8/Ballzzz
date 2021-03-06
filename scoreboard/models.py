import os
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get database URL from system env
DB_URL = os.environ.get('DATABASE_URL')

Base = declarative_base()

# Define DB object
class Scoreboard(Base):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)
    score = Column(Integer, nullable=False)

# Create DB connection
engine = create_engine(DB_URL)

# Create DB and and tables
Base.metadata.create_all(engine)
print('DB Created')

# DB Connector
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)()
