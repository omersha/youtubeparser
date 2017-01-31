#!/usr/bin/env python2

"""
Downloads list of videos from youtube (requires youtube-dl).
Usage: ytdownload.py file_with_videos_to_download
"""
 
import os
import argparse
from youtubeutils import capitalized_case, stringify_index

def download(url, targetpath, targetname):
    ydlexe = 'youtube-dl'
    target = targetname + '.%(ext)s'
    target = os.path.join(targetpath, target)
    os.system(ydlexe+' -f 18 ' + url + ' -o "' + target + '"')


def read_yt_file(filename, basepath):
    with open(filename) as f:
        lines = f.readlines()

    index = 1
    section = ''
    for line in lines:
        line = line.strip()
        if line[:8] == 'SECTION:':
            index = 1
            section = line[8:].strip()
            print 'Section = ', section
        else:
            name, url = line.split(';;')
            name = stringify_index(index) + ' ' + capitalized_case(name)
            url = url.strip()
            download(url, os.path.join(basepath, section), name)
            index = index + 1


def main():
    parser = argparse.ArgumentParser(description='YouTube Downloader')
    parser.add_argument('filename', nargs=1, help='instructions file-name')
    parser.add_argument('-p', '--path', dest='path', action='store',
                        type=str, help='target path', required=False)
    args = parser.parse_args()

    path = args.path if args.path is not None else './'
    read_yt_file(args.filename[0], path)
    
if __name__ == "__main__":
    main()


