#!/usr/bin/env python2

"""
Scraping and parsing an entire youtube channel for downloading.
Usage: ytchannel.py channel_id -s directory_name
"""


import urllib2
import argparse
from bs4 import BeautifulSoup
from youtubeutils import string2filename

def parse_youtube_channel(channel_id, include_names=[], execlude_names=[]):
    lines = []

    url = 'https://www.youtube.com/channel/%s/videos'%channel_id
    soup = BeautifulSoup(urllib2.urlopen(url), 'html.parser')
    items = soup.find_all('h3', {'class':'yt-lockup-title'})
    for item in items :
        video = item.find('a')
        video_name = video.get('title').strip()
        video_link = 'https://www.youtube.com%s'%video.get('href').strip()
        if include_names == [] or video_name in include_names:
            if execlude_names == [] or video_name not in execlude_names:
                lines.append(string2filename(video_name) + ' ;; ' + video_link)
    return '\n'.join(lines)

def dl_yt_channel(channel_id, path, section_name, include_names=[], execlude_names=[]):
    with open(path, 'w') as f:
        f.write('SECTION: %s\n'%section_name)
        f.writelines(parse_youtube_channel(channel_id, include_names, execlude_names))



def main():
    parser = argparse.ArgumentParser(description='YouTube channels parser')
    parser.add_argument('id', nargs=1, help='channel ID')
    parser.add_argument('-f', '--file', dest='file', action='store',
                        type=str, help='file-name', required=False)
    parser.add_argument('-s', '--section', dest='section', action='store',
                        type=str, help='section title', required=False)
    args = parser.parse_args()

    filename = args.file if args.file is not None else 'yt.list'
    section = args.section if args.section is not None else 'YouTubeList'
    print 'Parsing channel (ID=%s) into %s...'%(args.id[0], filename)
    dl_yt_channel(args.id[0], filename, section)

if __name__ == "__main__":
    main()


