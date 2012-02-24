#! /usr/bin/env python
import eyeD3
import sys
import urllib
import string
import re

# consumes a string s and returns the string with all punctuation characters deleted
def nopunc(s):
    return ''.join(e for e in s if e.isalnum())

def printlyrics(path):
    # set up a tag object
    tag = eyeD3.Tag()
    # map the tag to the ID3 of the file at the path given by the first command line    
    # argument
    tag.link(path)

    Artist = tag.getArtist()
    Title = tag.getTitle()

    # clean up the artist and title for use in the lyrics URL
    artist = nopunc(Artist.replace('The', '')).lower()
    title = nopunc(Title).lower()

    # construct the lyrics URL
    urlstring = "http://www.azlyrics.com/lyrics/{0}/{1}.html".format(artist, title)
    # get the HTML at the proper URL
    lyricsf = urllib.urlopen(urlstring)

    # clean up the HTML file
    try:
        lyrics = lyricsf.read().split('<!-- start of lyrics -->')[1]
    except IndexError:
        print "Sorry, no lyrics were found."
        return
        
    lyrics = lyrics.split('<!-- end of lyrics -->')[0]
    # remove HTML tags
    lyrics = re.sub('<.*?>', '', lyrics)

    print "{0} by {1}".format(Title, Artist)
    print lyrics

if len(sys.argv) < 2:
    print "Please provide path(s) to the song file(s) you would like the lyrics for."

for path in sys.argv[1:]:
    printlyrics(path)