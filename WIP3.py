# Main File where the audio is slowed or sped up, and reverb is added. A function to play the wav file from the terminal is also included

import simpleaudio as sa
import pydub, os, sox
from pydub import AudioSegment

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

def reverb(outFileName, verb = 0, hiFreqDamp = 50):
    infile = "intermediate.wav"
    outfile = outFileName + "﹝slowed + reverb﹞.mp3"

    tfm = sox.Transformer()

    tfm.reverb(reverberance=verb, high_freq_damping=hiFreqDamp, wet_gain=(verb*-0.10))

    tfm.build_file(infile, outfile)

def playWav(fileName):
    waveSound = sa.WaveObject.from_wave_file(fileName)
    playSound = waveSound.play()
    playSound.wait_done()

inFile = "Buffy.wav"
inFileName = inFile[:-4]
audioPydub = AudioSegment.from_file(inFile)

audioPydub = pitchSpeedChange(audioPydub, 0.85)

outFile = audioPydub.export("intermediate.wav", "wav")

reverb(inFileName, 87, 0)

finalFile = inFileName + "﹝slowed + reverb﹞.mp3"
song = AudioSegment.from_file(finalFile)

os.remove("intermediate.wav")

# songWav = song.export(inFileName + "﹝slowed + reverb﹞.wav", "wav")
# playWav(inFileName + "﹝slowed + reverb﹞.wav")
