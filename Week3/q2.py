from scipy import *
from matplotlib.pylab import *
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
from numpy.core.multiarray import array
from numpy.lib.function_base import append
import pyaudio, wave, sys, aifc
import numpy.fft as fft
import struct

CHANNELS = 1
chunk = 1024
FORMAT = pyaudio.paInt32
RATE = 44100

file = aifc.open("/Users/Jim/Desktop/week3/sound_files/F3_PopOrgan.aif","rb")
data = file.readframes(chunk)
#combine

integer_data = fromstring(data, dtype=np.int8)
#integer_data = fromstring(data, dtype=np.uint32)
integer_data=integer_data[::2]
trans = fft.fft(integer_data)
length = len(trans)
unique = ceil((length)/float(2))
#FFT is symmetric
trans = (abs(trans[0:unique])/float(length))**2
#Accounting for Nyquist point
if length % 2 > 0: # we've got odd number of points fft
      trans[1:len(trans)] = trans[1:len(trans)] * 2
else:
      trans[1:len(trans) -1] = trans[1:len(trans) - 1] * 2 # we've got even number of points fft
#getting correct frequency
freqArray = arange(0, unique, 1.0) #* (float(1024) / length)
plot(freqArray, 10*log10(trans), color='k')
plt.show()





"""

time = arange(size(trans)) / float(RATE)
plot_title = ("Audio Analysis")
fig = plt.figure(figsize=(7, 4.5))
ax1 = fig.add_subplot(1,1,1)
ax1.plot(time, integer_data, color="red", linestyle="-")
#ax1.set_xlabel("Time [s]")
#ax1.set_ylabel("Amplitude")
ax1.set_xlim(min(time), max(time))
ax1.set_title(plot_title)
show()


for i in range(0,len(data),4):
    val = struct.unpack('f',''.join(data[i:i+4]))[0]
    print val
    sound_file[i]=val
print sound_file
trans = fft.rfft(sound_file)

for i in range(0,len(data),8):
    val = struct.unpack('ff',''.join(data[i:i+8]))[0]
    break
"""
