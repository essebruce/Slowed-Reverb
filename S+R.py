from __future__ import unicode_literals
import pydub, os, sox, youtube_dl, argparse
import Functions as sr
from pydub import AudioSegment
import simpleaudio as sa

parser = argparse.ArgumentParser(description="Create a slowed + reverb mix of a song of your choice")
parser.add_argument("-s", "--speed", type=float, default=80, help="Input a percentage between 50 and 200 to indicate how slow or fast you want the track to be. Default is 80")
parser.add_argument("-r", "--reverb", type=int, default=50, help="Input an integer between 0 and 100 to indicate how much reverb you want to add. Default is 50")
parser.add_argument("song",  type=str, help="Input a link to the youtube video you want to slow down - \'youtube link\'.  Must be have single quotes around string.")
parser.add_argument("-a", "--fileAddOn", type=str, default="﹝slowed + reverb﹞", help="String that will be added onto the end of the slowed + reverb file in parentheses. Default is \'﹝slowed + reverb﹞\'. Must be have single quotes around string.")
parser.add_argument("--hfqd", type=int, default=30, help="Input an integer between 0 and 100 to indicate how much high frequency dampening you want to add. Default is 30")
parser.add_argument("--scale", type=int, default=100, help="Input an integer between 0 and 100 to indicate the room scale of the reverb. Default is 100")
args = parser.parse_args()

youtubeLink = args.song
fileNameAddOn = args.fileAddOn
if (args.fileAddOn != '﹝slowed + reverb﹞'):
    fileNameAddOn = " (" + args.fileAddOn + ")"
trackSpeed = (args.speed)/100.0
reverbAmount = args.reverb
hiFreqDampAmount = args.hfqd
roomScale = args.scale

inFile = sr.youtubeDL(youtubeLink) + ".mp3"
inFileName = inFile[:-4]
audioPydub = AudioSegment.from_file(inFile)

audioPydub = sr.pitchSpeedChange(audioPydub, trackSpeed)

intermediateFile = inFileName + "Slowed.wav"

audioPydub.export(intermediateFile, "wav")

outFileName = inFileName + fileNameAddOn + ".mp3"

sr.reverb(inFileName, outFileName, reverbAmount, hiFreqDampAmount, roomScale)

song = AudioSegment.from_file(outFileName)

os.remove(intermediateFile)
os.remove(inFile)

# songWav = song.export(inFileName + "﹝slowed + reverb﹞.wav", "wav")
# playWav(inFileName + "﹝slowed + reverb﹞.wav")