import soundfile as sf, pyrubberband as pyrb

y, sr = sf.read('Buffy.wav')

yPitchShift = pyrb.pitch_shift(y, sr, -5)

sf.write('BuffyShifted.wav', yPitchShift, sr)