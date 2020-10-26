from __future__ import unicode_literals
import pydub, os, sox, youtube_dl
from pydub import AudioSegment
import simpleaudio as sa


# Function which changes both speed and pitch of a pydub audio instance. Takes a pydub instance of audio, and a double for the audio speed
# Taken from Stack Overflow user Jiaaro, who explains the logic in the comments of the function: https://stackoverflow.com/questions/43408833/how-to-increase-decrease-playback-speed-on-wav-file
# Essentially, you change the framerate of the song, and then resample it at 44.1k hz to allow it to be played
def pitchSpeedChange(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)
      })
     # convert the sound with altered frame rate to a standard frame rate
     # so that regular playback programs will work right. They often only
     # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

# Reverb function takes the name of the original audio, name of the outbound file, and values for the amount of reverb, high frequency dampening, and room scale
# Utilizes the SoX set of effects to apply reverb through an effects chain which just includes a reverb module
# Since Reverb adds to the gain of a track, the wet gain is reduced based on the amount of reverb added to the track to prevent clipping (i.e. a reverb value of 100 reduces the wet gain by 10 db).
# Creates the outbound file at the end
def reverb(inFileName, outFileName, verb = 50, hiFreqDamp = 50, roomScale = 100):
    infile = inFileName + "Slowed.wav"
    outfile = outFileName

    tfm = sox.Transformer()

    tfm.reverb(reverberance=verb, high_freq_damping=hiFreqDamp, wet_gain=(verb*-0.10), room_scale=roomScale)

    tfm.build_file(infile, outfile)

# 
def youtubeDL(link):
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

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
        vidInfo = ydl.extract_info(url = link, download=False)
        videoTitle = vidInfo.get('title', None)
        return videoTitle

def playWav(fileName):
    waveSound = sa.WaveObject.from_wave_file(fileName)
    playSound = waveSound.play()
    playSound.wait_done()