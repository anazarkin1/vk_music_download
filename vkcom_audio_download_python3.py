import json
import re
import os
import requests
import csv
import sys


FORBIDDEN_CHARS = '/\\\?%*:|"<>!'
MUSIC_FOLDER = 'music'

def read_csv_file(filename):
    with open(filename, newline='') as csvfile:
       audiolist = csv.reader(csvfile, delimiter= ',', quotechar='"')
       for row in audiolist:
         find_track(row)


def find_track(csv_row):
    #csv_row[0] - songname, csv_row[1] - artistname
    filename = csv_row[0]+' - '+ csv_row[1]
    filename = re.sub('[' + FORBIDDEN_CHARS + ']', "", filename)
    filename = re.sub(' +', ' ', filename)
    filename= filename+'.mp3'
    print(filename)
    TOKEN = sys.argv[2]

    #sort = 2 by popularity, auto_complete=1 fixes potential typos
    params = dict(q=csv_row[0] + ' ' +csv_row[1], sort = 2, auto_complete=1, access_token=TOKEN)
    url = "https://api.vk.com/method/audio.search"
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    urlD = data['response'][1]['url']

    if download_file(urlD, filename) == filename:
        print("***", filename," downloaded")


##courtesy of Roman Podlinov
#http://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
#
def download_file(url, filename):
    if filename=="":
        local_filename = url.split('/')[-1]
    else:
        local_filename = filename
    local_filename = os.path.join(MUSIC_FOLDER or "", local_filename)
   # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename


def main():
    if MUSIC_FOLDER and not os.path.exists(MUSIC_FOLDER):
        os.makedirs(MUSIC_FOLDER)

    #expects 1st argument to be filename
    #             2nd argument to be token
    filename = sys.argv[1]
    print(filename)
    read_csv_file(filename)



if __name__ == '__main__':
    main()
