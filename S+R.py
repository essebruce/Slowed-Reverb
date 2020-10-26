from __future__ import unicode_literals
import pydub, os, sox, youtube_dl, argparse
import Functions as sr
from pydub import AudioSegment
import simpleaudio as sa

# Create a command line parser with arguments to capture speed, reverb, an alternate file ending, high frequency dampening value,
# and the song link

parser = argparse.ArgumentParser(description="Create a slowed + reverb mix of a song of your choice")
parser.add_argument("-s", "--speed", type=float, default=80, help="Input a percentage between 50 and 200 to indicate how slow or fast you want the track to be. Default is 80")
parser.add_argument("-r", "--reverb", type=int, default=50, help="Input an integer between 0 and 100 to indicate how much reverb you want to add. Default is 50")
parser.add_argument("song",  type=str, help="Input a link to the youtube video you want to slow down - \'youtube link\'.  Must be have single quotes around string.")
parser.add_argument("-f", "--fileAddOn", type=str, default="﹝slowed + reverb﹞", help="String that will be added onto the end of the slowed + reverb file in parentheses. Default is \'﹝slowed + reverb﹞\'. Must be have single quotes around string.")
parser.add_argument("--hfqd", type=int, default=50, help="Input an integer between 0 and 100 to indicate how much high frequency dampening you want to add. Default is 30")
parser.add_argument("--scale", type=int, default=100, help="Input an integer between 0 and 100 to indicate the room scale of the reverb. Default is 100")
parser.add_argument("-k", "--keep", type=str, default='False', help="Put in 'True' to keep the original song file on your directory")
args = parser.parse_args()

# Set variables to the argument values

youtubeLink = args.song
fileNameAddOn = args.fileAddOn
if (args.fileAddOn != '﹝slowed + reverb﹞'):
    fileNameAddOn = " (" + args.fileAddOn + ")"
trackSpeed = (args.speed)/100.0
reverbAmount = args.reverb
hiFreqDampAmount = args.hfqd
roomScale = args.scale

# Downloads the mp3 version of the youtube link and creates a pydub instance of the audio

inFile = sr.youtubeDL(youtubeLink) + ".mp3"
inFileName = inFile[:-4]
audioPydub = AudioSegment.from_file(inFile)

# Slow down (or speed up if the value of trackSpeed is greater than 1) the audio and create an intermediate .wav file

audioPydub = sr.pitchSpeedChange(audioPydub, trackSpeed)

intermediateFile = inFileName + "Slowed.wav"

audioPydub.export(intermediateFile, "wav")

outFileName = inFileName + fileNameAddOn + ".mp3"

# Add reverb to the track

sr.reverb(inFileName, outFileName, reverbAmount, hiFreqDampAmount, roomScale)

song = AudioSegment.from_file(outFileName)

# Remove the orginal audio file and the intermediate file from the directory

os.remove(intermediateFile)
if ((args.keep) == 'False'):
    os.remove(inFile)

# Plays a .wav version of the final product from the terminal (Used while testing the functions during development)
# songWav = song.export(inFileName + "﹝slowed + reverb﹞.wav", "wav")
# playWav(inFileName + "﹝slowed + reverb﹞.wav")