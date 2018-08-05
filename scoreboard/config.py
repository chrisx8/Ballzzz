from common import create_session_key
import os

# Generate secret key
# Syntax: SECRET_KEY=create_session_key(length)
SECRET_KEY=create_session_key(50)

# Database
# SQLite: 'sqlite:///database.db'
# MySQL: 'mysql+mysqlconnector://username:password@host:port/database'
# PostgreSQL: 'postgresql://scott:tiger@localhost/mydatabase'
DATABASE_URL = os.environ['DATABASE_URL']
