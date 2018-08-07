# Ballzzz Scoreboard

This folder contains the scoreboard webapp for Ballzzz.

## Configure game to use a our server

You don't have to change anything to upload your score to our score server!

## Optional: Deploy your own scoreboard server

### Run with a virtual environment

**The following steps are supported on MacOS and Linux. Windows is NOT SUPPORTED!**

Run the following in your command line (`Terminal.app` on MacOS)

```bash
# Clone project source from Git
git clone https://github.com/chrisx8/Ballzzz.git
cd PyTetris/scoreboard

# Install pip before continuing
# Install virtualenv
pip install --user virtualenv

# Create a virtual environment
virtualenv pytetris-env

# Activate environment
source pytetris-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
# Change 0.0.0.0:8000 to something else if you don't want the server on port 8000, or you don't want the server to be accessible from everywhere.
gunicorn wsgi:app -b 0.0.0.0:8000
```

### Run directly

**The following steps are supported on MacOS and Linux. Windows is NOT SUPPORTED!**

Running with a virtual environment is HIGHLY RECOMMENDED, as running directly can make removing installed packages VERY difficult.

```bash
# Clone project source from Git
git clone https://github.com/chrisx8/PyTetris.git
cd PyTetris/scoreboard

# Install pip before continuing
# Install dependencies
pip install --user -r requirements.txt

# Run server
# Change 0.0.0.0:8000 to something else if you don't want the server on port 8000, or you don't want the server to be accessible from everywhere.
gunicorn wsgi:app -b 0.0.0.0:8000
```

### Run with Docker

Coming soon!
