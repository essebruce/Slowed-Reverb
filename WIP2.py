# File to create the youtube download function and pass the file title

from __future__ import unicode_literals
import youtube_dl

class MyLogger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

videoLink = 'https://www.youtube.com/watch?v=75lmWibgctI'
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([videoLink])
    vidInfo = ydl.extract_info(url = videoLink, download=False)
    videoTitle = vidInfo.get('title', None)
    print(videoTitle)
