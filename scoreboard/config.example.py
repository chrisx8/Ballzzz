# DO NOT CHANGE THESE
from common import create_session_key
import os
SECRET_KEY=create_session_key(50)

# Database Connection
# SQLite: 'sqlite:///database.db'
# MySQL: 'mysql+mysqlconnector://username:password@host:port/database'
# PostgreSQL: 'postgresql://username:password@host:port/database'
DATABASE_URL = ''
