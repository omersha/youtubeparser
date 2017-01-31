#!/usr/bin/env python2

"""
Scraping and parsing a youtube's videos list for downloading.
Usage: ytlist.py list_id -s directory_name
"""
 

from youtubeutils import string2filename
import urllib2
import argparse
from bs4 import BeautifulSoup

def _parse_youtube_list_rows(rows, lines):
    for row in rows:
        video = row.find('td', {'class':'pl-video-title'}).find('a')
        video_name = video.text.strip()
        video_link = 'https://www.youtube.com' + video.get('href').split('&')[0]
        lines.append(string2filename(video_name) + ' ;; ' + video_link)
    return lines

def _parse_youtube_list_loadmore(soup, lines):
    btns= soup.select('button.load-more-button')
    if len(btns) == 0:
        return lines
    elif len(btns) != 1:
        print 'Weird! Take note'
    ajax = 'https://www.youtube.com'+btns[0]['data-uix-load-more-href']
    resjson = json.loads(BeautifulSoup(urllib2.urlopen(ajax)).text)
    rows = BeautifulSoup(resjson['content_html'], 'html.parser').find_all('tr')
    return _parse_youtube_list_rows(rows, lines)


def parse_youtube_list(list_id):
    lines = []

    url = 'https://www.youtube.com/playlist?list='+list_id
    soup = BeautifulSoup(urllib2.urlopen(url), 'html.parser')
    table = soup.find('table', id='pl-video-table')
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    lines = _parse_youtube_list_rows(rows, lines)
    lines = _parse_youtube_list_loadmore(soup, lines)
    return u'\n'.join(lines)
 

def dl_yt_list(list_id, path, section_name):
    with open(path, 'w') as f:
        f.write('SECTION: %s\n'%section_name)
        f.writelines(parse_youtube_list(list_id))
   

def main():
    parser = argparse.ArgumentParser(description='YouTube lists parser')
    parser.add_argument('id', nargs=1, help='list ID')
    parser.add_argument('-f', '--file', dest='file', action='store',
                        type=str, help='file-name', required=False)
    parser.add_argument('-s', '--section', dest='section', action='store',
                        type=str, help='section title', required=False)
    args = parser.parse_args()

    filename = args.file if args.file is not None else 'yt.list'
    section = args.section if args.section is not None else 'YouTubeList'
    print 'Parsing list (ID=%s) into %s...'%(args.id[0], filename)
    dl_yt_list(args.id[0], filename, section)
    
if __name__ == "__main__":
    main()


