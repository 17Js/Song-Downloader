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

# Configuration variables
songspath = input('Song file: ') + '.txt' # './songs.txt'  # Location of the song list to download
savepath = input('Output folder: ') # './songs/' # Location to save the songs

# Get list of songs to download
songlist = removeNewlines(open(songspath, 'r').readlines())

threads = []
for song in songlist:
    threads.append(threading.Thread(target=downloadSong, args=(song, savepath)))

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print(f'All {len(songlist)} songs downloaded in {ts(stamp)}')