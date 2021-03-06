#!/usr/bin/python3

import time
import requests
import sys
import os.path
import logging
from itertools import zip_longest

logging.basicConfig(level=logging.DEBUG)

ua_file = "user-agent.txt"
if os.path.isfile(ua_file):
    with open(ua_file, "r") as f:
        try:
            ua = next(f).strip()
        except Exception as e:
            logging.warning("Couldn't read user agents file; " +
                "make sure you have at least one line of text in " +
                ua_file)
            ua = ""
    HEADERS = {
        'User-Agent': ua + ' BasedOnpython-requests/' + str(requests.__version__),
    }
else:
    HEADERS = {}

NAMESPACES_MAP = {
        "Main": 0,
        "Talk": 1,
        "User": 2,
        "User talk": 3,
        "Wikipedia": 4,
        "Wikipedia talk": 5,
        "File": 6,
        "File talk": 7,
        "MediaWiki": 8,
        "MediaWiki talk": 9,
        "Template": 10,
        "Template talk": 11,
        "Help": 12,
        "Help talk": 13,
        "Category": 14,
        "Category talk": 15,
        "Portal": 100,
        "Portal talk": 101,
        "Book": 108,
        "Book talk": 109,
        "Draft": 118,
        "Draft talk": 119,
        "Education Program": 446,
        "Education Program talk": 447,
        "TimedText": 710,
        "TimedText talk": 711,
        "Module": 828,
        "Module talk": 829,
        "Gadget": 2300,
        "Gadget talk": 2301,
        "Gadget definition": 2302,
        "Gadget definition talk": 2303,
}

NAMESPACES_INV_MAP = {v: k for k, v in NAMESPACES_MAP.items()}

NAMESPACES = list(NAMESPACES_MAP.keys())

# Modified from https://www.mediawiki.org/wiki/API:Query#Continuing_queries
def query(request, lang="en", sleep=1):
    request['action'] = 'query'
    request['format'] = 'json'
    lastContinue = {'continue': ''}
    iteration = 0
    while True:
        # Clone original request
        req = request.copy()
        # Modify it with the values returned in the 'continue' section of the
        # last result.
        req.update(lastContinue)
        # Call API
        r = requests.get('https://{}.wikipedia.org/w/api.php'.format(lang),
                params=req, headers=HEADERS)
        result = r.json()
        logging.info("ON ITERATION %s, SLEEPING FOR %s", iteration, sleep)
        time.sleep(sleep)
        iteration += 1
        if 'error' in result:
            raise ValueError(r.url, result['error'])
        if 'warnings' in result:
            logging.warning(result['warnings'])
        if 'query' in result:
            yield result['query']
        if 'continue' not in result:
            break
        lastContinue = result['continue']

# From https://docs.python.org/3/library/itertools.html#itertools-recipes
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
