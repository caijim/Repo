import numpy as np
import numpy.fft as fft
import matplotlib.mlab as mlab
from pylab import imread, imshow, gray, mean
from matplotlib import pyplot as plt
from pylab import specgram
import pylab as py

a = imread('moonlanding.png')
trans = fft.rfft2(a)
power = np.abs(a)**2
#high = mlab.prctile(abs(trans.flatten()),p=[95])[0]
high = mlab.prctile(abs(trans.flatten())[:len(trans.flatten())//2], p=[95])[0]
print high

"""
trans = abs(trans)
plt.hist(abs(trans.flatten()),range= [trans.mean()-.10*trans.std(), trans.mean()+.10*trans.std()], normed =1)
#plt.hist(trans))
plt.gray()
plt.show()
"""

count = 0
dimx, dimy = len(trans), len(trans[1])
blah = trans.flatten()
for i in range(len(blah)):
    if abs(blah[i]) >= high:
        blah[i] = 0
        count+=1
trans = blah.reshape(dimx, dimy)
#plt.plot(trans.real, trans.imag,',')
#plt.show()

specgram( abs(trans.flatten()))
plt.show()
invfft = abs(fft.irfft2(trans))
plt.imshow(invfft)
plt.gray()
plt.show()






