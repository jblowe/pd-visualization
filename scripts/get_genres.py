# -*- coding: utf-8 -*-

# Description: retrieves the genre of items; attempts to normalize genre text
# Example usage:
#   python get_genres.py ../data/src/pd_items.json ../data/genres.json ../data/item_genres.json

import Counter
import json
from pprint import pprint
import re
import sys
import urllib

# input
if len(sys.argv) < 3:
    print "Usage: %s <inputfile items json> <outputfile genres json> <outputfile item genres json>" % sys.argv[0]
    sys.exit(1)
INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
OUTPUT_ITEMS_FILE = sys.argv[3]

# if string contains [x]: replace with [y]
substrings = {
    'lithograph': 'lithographs',
    'lithogrpah': 'lithographs',
    'litograph': 'lithographs',
    'lithgraph': 'lithographs',
    'engraving': 'engravings',
    'engraing': 'engravings',
    'engraver': 'engravings',
    'print': 'prints',
    'etching': 'etchings',
    'drawing': 'drawings',
    'pencil': 'drawings',
    'watercolor': 'watercolors',
    'gouache': 'watercolors',
    'ink': 'drawings',
    'photograph': 'photographs',
    'book': 'books',
    'monograph': 'books',
    'atlas': 'atlases',
    'painting': 'paintings',
    'illustration': 'illustrations',
    'map': 'maps',
    'cartographic': 'maps',
    'pen': 'drawings',
    'manuscript': 'manuscripts',
    'document': 'documents',
    'scroll': 'scrolls',
    'scores': 'sheet music',
    'musical notation': 'sheet music'
}

# init
genres = []
item_genres = []
urltemplate = "https://webapps.cspace.berkeley.edu/pahma/search/search/?fcp_qualifier=keyword&displayType=list&maxresults=50&start=1i&fcp="

def addGenre(g):
    global genres
    global item_genres

    genre = next(iter([_g for _g in genres if _g['value']==g]), False)

    if genre:
        genres[genre['index']]['count'] += 1
    else:
        label = 'Unknown'
        url = ''
        if g:
            label = g
            url = urltemplate + urllib.quote(label)
        genre = {
            'index': len(genres),
            'value': g,
            'label': label,
            'url': url,
            'count': 1
        }
        genres.append(genre)

    item_genres.append(genre['index'])

for line in open(INPUT_FILE,'rb').readlines():
    # Read line
    items = line.split('\t')

    # Retrieve genre
    genrex = items[41].split('|')
    genre = genrex[1] if len(genrex) > 1 else genrex[0]
    addGenre(genre)

# Report on collections
genres = sorted(genres, key=lambda d: d['count'], reverse=True)
genres = [ g for g in genres if g['count'] > 10 ]
pprint(genres)

# Write out data
with open(OUTPUT_FILE, 'w') as outfile:
    json.dump(genres, outfile)
print "Wrote " + str(len(genres)) + " genres to " + OUTPUT_FILE

with open(OUTPUT_ITEMS_FILE, 'w') as outfile:
    json.dump(item_genres, outfile)
print "Wrote " + str(len(item_genres)) + " items to " + OUTPUT_ITEMS_FILE
