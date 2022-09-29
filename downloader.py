#!/usr/bin/env python

# ---------------Usage---------------
#           > python3 downloader.py
# > Song list: {The file of the songs you would like to download
#               Adds .txt extension if none is given}
# > Output folder: {The location of the folder where the songs are downloaded to
#                   Makes a new folder if there is none}

# Import packages
from datetime import datetime
from pytube import YouTube
import urllib.request
import threading
import re
import os

# Download the song into the specified location
def downloadSong(song, location):
    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + song.replace(' ', '+'))
    results = re.findall(r'watch\?v=(\S{11})', html.read().decode())
    url = ('https://www.youtube.com/watch?v=' + results[0])
    song = YouTube(url)
    video = song.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=location)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

# Remove newlines from each item in a list
def removeNewlines(list):
    newlist = []
    for item in list:
        i = item.replace('\n', '')
        newlist.append(i)
    return newlist

def ts(stamp):
    delta = str(datetime.now() - stamp)
    stamp = datetime.now()
    return delta

stamp = datetime.now()

# Configuration
listpath = input('Song list: ')
savepath = input('Output folder: ')

# Check if the song file has an extension, if not, add .txt
if ('.' not in listpath[1:]):
    listpath += '.txt'

# Get list of songs to download
songlist = removeNewlines(open(listpath, 'r').readlines())

threads = []
for song in songlist:
    threads.append(threading.Thread(target=downloadSong, args=(song, savepath)))

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print(f'All {len(songlist)} songs downloaded in {ts(stamp)}')
