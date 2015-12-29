#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""urlmon.py
Python script to monitor a webpage component for changes.
"""

import sys
import os.path
import argparse
import keyring
import re
from urllib.parse import urlparse
import requests
import logging
from difflib import unified_diff

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
        )

logging.getLogger("requests").setLevel(logging.WARNING)

logger_name = str(__file__) + " :: " + str(__name__)
logger = logging.getLogger(logger_name)


class Pushover(object):
    """Pushover client"""
    def __init__(self, api_token, user):
        self.api_token = api_token
        self.user = user

    def push(self, message, device=None, title=None, url=None, url_title=None,
             priority=None, timestamp=None, sound=None):
        """Pushes the notification.

        Arguments:
            message -- your message

        Keyword arguments:
            device -- your user's device name to send the message directly to
                that device, rather than all of the user's devices
            title -- your message's title, otherwise your app's name is used
            url -- a supplementary URL to show with your message
            url_title -- a title for your supplementary URL, otherwise just the
                URL is shown
            priority -- send as --1 to always send as a quiet notification, 1
                to display as high--priority and bypass the user's quiet hours,
                or 2 to also require confirmation from the user
            timestamp -- a Unix timestamp of your message's date and time to
                display to the user, rather than the time your message is
                received by our API
            sound -- the name of one of the sounds supported by device clients
                to override the user's default sound choice.
        """

        api_url = 'https://api.pushover.net/1/messages.json'

        payload = {
            'token': self.api_token,
            'user': self.user,
            'message': message,
            'device': device,
            'title': title,
            'url': url,
            'url_title': url_title,
            'priority': priority,
            'timestamp': timestamp,
            'sound': sound
        }

        return requests.post(api_url, params=payload).status_code


def diff(first, second):
    """Return a diff of the two strings"""
    return '\n'.join(unified_diff(first.splitlines(), second.splitlines()))


def main(arguments):
    """Parse arguments, request the urls, notify if different."""
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=formatter_class)
    parser.add_argument('infile', help="Input file",
                        type=argparse.FileType('r'))
    parser.add_argument('-o', '--outfile', help="Output file",
                        default=sys.stdout, type=argparse.FileType('w'))
    args = parser.parse_args(arguments)

    urls = args.infile.read().splitlines()

    api_token = keyring.get_password('pushover', 'api_token')
    pushover_user = keyring.get_password('pushover', 'user')
    pushover = Pushover(api_token, pushover_user)

    for url in urls:
        domain = urlparse(url).netloc
        urlpath = urlparse(url).path
        url_dashes = re.sub(r'/', '-', urlpath)
        filename = domain + url_dashes + '.html'
        filepath = os.path.join('cache', filename)

        html = requests.get(url).text

        if os.path.isfile(filepath):
            with open(filepath) as r:
                before = r.read()
            if html == before:
                logger.info("{} is unchanged".format(url))
            else:
                msg = "{} changed".format(url)
                logger.info(msg)
                logger.debug(diff(before, html))
                pushover.push(msg)
                logger.debug("Pushover notification sent")

        else:
            with open(filepath, 'w') as w:
                w.write(html)
            logger.info("Wrote file to cache/: {}".format(filename))


def _cli():
    sys.exit(main(sys.argv[1:]))

if __name__ == '__main__':
    _cli()
