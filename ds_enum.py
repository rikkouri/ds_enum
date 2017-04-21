#!/usr/bin/python

import argparse
import urllib as urllib
from urllib import urlopen, FancyURLopener
from StringIO import StringIO
from ds_store import DSStore, buddy
import logging
from logging import error, info, warning

__version__ = "0.1"


class CustomBrowser(FancyURLopener):
    version = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2622.87 Safari/537.36"


def valid_url(url, strict=False):
    request = urllib.urlopen(url)
    code = request.getcode()
    request.close()
    # If strict we only want to return true on a 200 response.
    if strict:
        return code == 200
    else:
        return code != 404


def parse_dsstore(file):
    try:
        store = DSStore.open(file)
    except buddy.BuddyError:
        print "[!] Unable to parse DS Store file."
        return []
    return store.__iter__()


def open_dsstore(url):
    print "[ ] Downloading... '%s'" % url
    if not valid_url(url):
        return False

    browser = CustomBrowser()
    response = browser.open(url)
    data = response.read()
    store_file = StringIO()
    store_file.write(data)
    store_file.flush()
    return store_file


def process_url(url, results=[], depth=0, max_depth=3):
    print "[ ] Processing... '%s'" % url
    store = open_dsstore(url)
    root_url = url.replace('.DS_Store', '')

    if not store:
        return

    items = parse_dsstore(store)

    if not items:
        return

    for item in items:
        print "[?] Item: %s" % item
        location = root_url + item.filename

        if location not in results:
            results.append(location)

            if len(item.filename) > 4 and (item.filename[-4] != '.'):
                process_url(location + "/.DS_Store", results)

    return results

parser = argparse.ArgumentParser()
parser.add_argument("base_url", help="starting point")
parser.add_argument("-v", "--verbose", help="verbose mode", action="store_true")
parser.add_argument("-t", "--timeout", help="max timeout in milliseconds", type=int, default=300)
args = parser.parse_args()

base_url = args.base_url
verbose = args.verbose
timeout = args.timeout


logging.info("Verbose mode")

exit(1)
print "Checking base URL..."
#if not valid_url(base_url, strict=True):
#    print "invalid url"
#    exit(1)

urls = process_url(base_url)

for url in urls:
    print "[+] %s" % url