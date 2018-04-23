# -*- coding: utf-8 -*-

# Description: retrieves the date (year or century) of items
# Example usage:
#   python get_dates.py ../data/src/pd_items.json ../data/dates.json ../data/item_dates.json year
#   python get_dates.py ../data/src/pd_items.json ../data/centuries.json ../data/item_centuries.json century

import Counter
import json
import math
from pprint import pprint
import re
import sys

# input
if len(sys.argv) < 4:
    print "Usage: %s <inputfile items json> <outputfile dates json> <outputfile item dates json> <time unit>" % sys.argv[0]
    sys.exit(1)
INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
OUTPUT_ITEMS_FILE = sys.argv[3]
TIME_UNIT = sys.argv[4]

urltemplate = 'https://webapps.cspace.berkeley.edu/pahma/search/search/?colldate=%s??&colldate_qualifier=keyword&displayType=list&maxresults=50&start=1'

# config
yearPattern = '[^0-9]*([12][0-9]{3}).*'
minYear = 1000
maxYear = 2018

# init
dates = []
item_dates = []

# Get a year from string
def getYearFromString(d):
    # Make everything a string
    if isinstance(d, (int, long, float)):
        d = str(d)
    # Case: 170 becomes 1700
    if len(d) < 4:
        d = d.ljust(4, '0')
    # Look for first year in standard format (e.g. 1900)
    match = re.search(yearPattern, d)
    if match:
        return int(match.group(1))
    # Case: 17-- becomes 1700, 179? becomes 1790
    d = d.replace('-', '0')
    d = d.replace('?', '0')
    match = re.search(yearPattern, d)
    if match:
        return int(match.group(1))
    # Case: 17th century becomes 1600
    match = re.search('[^0-9]*([12][0-9])th.*', d)
    if match:
        century = int(match.group(1))
        century -= 1
        return century * 100
    return False

def addDate(d):
    global dates
    global item_dates
    global TIME_UNIT

    date = next(iter([_d for _d in dates if _d['value']==d]), False)

    if date:
        dates[date['index']]['count'] += 1
    else:
        label = 'Unknown'
        url = ''
        if d:
            label = str(d)
            url = urltemplate % label
            if TIME_UNIT == 'century':
                if d==21:
                    label += "st century"
                else:
                    label += "th century"
                url = urltemplate % str(d)
        date = {
            'index': len(dates),
            'value': d,
            'label': label,
            'url': url,
            'count': 1
        }
        dates.append(date)

    item_dates.append(date['index'])



for line in open(INPUT_FILE,'rb').readlines():
    # Read line
    items = line.split('\t')

    # Retrieve date
    date = items[51]
    if 'colldate' in date: date = ''

    if date != '':

            year = int(date)
            if year and year > minYear and year < maxYear:
                date = year
                if TIME_UNIT == 'century':
                    date = int(math.floor(1.0 * year / 100)) + 1
        # if not date:
        #     print "No date found for: "
        #     pprint(item["date"])

    addDate(date)

# Report on dates
dates = sorted(dates, key=lambda d: d['value'])
pprint(dates)

# Write out data
with open(OUTPUT_FILE, 'w') as outfile:
    json.dump(dates, outfile)
print "Wrote " + str(len(dates)) + " dates to " + OUTPUT_FILE

with open(OUTPUT_ITEMS_FILE, 'w') as outfile:
    json.dump(item_dates, outfile)
print "Wrote " + str(len(item_dates)) + " items to " + OUTPUT_FILE
