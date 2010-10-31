from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
import numpy as np
import random, csv
#Plot Google, Yahoo Stock price data alongside NY high temperature

#Read in data
google = open("google_data.csv",'rU')
temps =  open("ny_temps.csv",'rU')
yahoo = open("yahoo_data.csv",'rU')
goog_data = np.loadtxt(google, dtype={'names': ('Modified Julian Date', 'Stock Value' ),'formats': ( 'f4', 'f4')},skiprows=1, delimiter=',')
temp_data = np.loadtxt(temps, dtype = {'names':('Modified Julian Date','Max Temperature'),'formats':('f4','f4')},skiprows=1, delimiter=',')
yahoo = np.loadtxt(yahoo, dtype = { 'names':('Modified Julian Date', 'Stock Value'),'formats': ( 'f4', 'f4')}, skiprows=1, delimiter=',')

dateStr= 'Modified Julian Date'
fig = plt.figure(figsize=(15,10))
host = fig.add_subplot(111)
par1 = host.twinx() #For labelling right y axis

#Labels
host.set_xlabel("Date(MJD)",size="large")
host.set_ylabel("Value(Dollars)",size="large")
par1.set_ylabel("Temperature( $\\degree $F)",size="large")
host.set_title("New York Temperature, Google, and Yahoo!", size="x-large",weight='bold')
p1, = host.plot(goog_data[dateStr], goog_data['Stock Value'],'blue', label="Google Stock Value",lw=2)
p2, = par1.plot(temp_data[dateStr], temp_data['Max Temperature'],'r--', label="NY Mon. High Temp",lw=2)
p3, = host.plot(yahoo[dateStr],yahoo['Stock Value'] ,'purple', label="Yahoo! Stock value",lw=2)

host.set_ylim(0, 765)
par1.set_ylim(-150, 100)
#frameon is not a kwarg in my version of matplotlib, so can't turn box off in legend
plt.legend((p1,p2,p3),('Google Stock Value','NY Mon. High Temp',"Yahoo! Stock value"), 'center left', numpoints=8 )
#Minor tick marks
host.xaxis.set_minor_locator(MultipleLocator(100))
host.yaxis.set_minor_locator(MultipleLocator(20))
par1.yaxis.set_minor_locator(MultipleLocator(10))
#Saving as q2.png
canvas = FigureCanvasAgg(fig)
canvas.print_figure("q2.png",dpi=144)
plt.draw()
plt.show()


