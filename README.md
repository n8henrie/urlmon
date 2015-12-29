# urlmon

**Work in progress.** Python script to monitor a webpage component for
changes.

-   Free software: MIT
-   Documentation: ~~https://urlmon.readthedocs.org~~

## Features

- Checks for changes in a website (or list of websites) since last run
- Sends a Pushover notification if there have been changes

## Installation

- Get a [Pushover API token](https://pushover.net/apps/build) (and your `user`
  info)
```bash
git clone https://github.com/n8henrie/urlmon.git
cd urlmon
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .

# Enter your Pushover API token:
keyring set pushover api_token

# Enter your Pushover user:
keyring set pushover user
```

## Usage

- Take single URL from stdin: `echo 'http://n8henrie.com' | python3 urlmon -`
- Take multiple URLs from file: `urlmon urls.txt`
