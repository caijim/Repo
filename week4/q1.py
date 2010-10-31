from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import random

#Fit a curve to the sample means 
#A sample is 25 points from a gaussian with mu=0, sigma = 25
fig = plt.figure()
host = fig.add_subplot(111)
points = 100000*25
sample = np.zeros(points)
means = np.zeros(float(points)/float(25))
for i in range(len(sample)):
    sample[i] = random.normalvariate(mu=0, sigma = 10)
reshaped = sample[:].reshape(float(points)/float(25), 25)
for row in range(len(reshaped)):
    means[row] = np.mean( reshaped[row])
count, bins, ignored = host.hist(means, 60, normed=True)
host.plot(bins,1/(2 * np.sqrt(2 * np.pi)) *np.exp( - (bins)**2 / (2 *2**2) ),linewidth=2, color='r')
v = host.axis()
v +=.1*np.array(v)
host.axis(list(v))
host.set_xlabel('Sample Means')
host.set_ylabel('Density')
host.set_title('Histogram of Sample Means')
canvas = FigureCanvasAgg(fig)
#Saving as q1.png
canvas.print_figure("q1.png",dpi=144)
fig.show()


