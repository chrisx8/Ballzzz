# Ballzzz Scoreboard

This folder contains the scoreboard webapp for Ballzzz.

## Configure game to use a our server

You don't have to change anything to upload your score to our score server!

## Optional: Deploy your own scoreboard server

### Supported databases

Use the following database URL formats when providing database URL:

- SQLite: `sqlite:///database.db`
- MySQL: `mysql://username:password@host:port/database`
- PostgreSQL: `postgres://username:password@host:port/database`

### Run in Docker

**Please install Docker before continuing.**

```bash
# Specify your database URL here
# Change 0.0.0.0:8000 to whatever you want your server to listen at
docker run -d -p 0.0.0.0:8000:8000 -e DATABASE_URL=YOUR_DATABASE_URL chrisx8/ballzzz-scoreboard:latest
```

### Run with a virtual environment

**The following steps are supported on MacOS and Linux. Windows is NOT SUPPORTED!**

```bash
# Clone project source from Git
git clone https://github.com/chrisx8/Ballzzz.git
cd Ballzzz/scoreboard

# Install pip before continuing
# Install virtualenv
pip install --user virtualenv

# Create a virtual environment
virtualenv ballzzz-env

# Activate environment
source ballzzz-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
# Specify your database URL here
# Change 0.0.0.0:8000 to whatever you want your server to listen at
DATABASE_URL = 'YOUR_DATABASE_URL' gunicorn wsgi:app -b 0.0.0.0:8000
```
