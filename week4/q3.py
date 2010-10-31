from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.ticker import MultipleLocator, MaxNLocator
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import random, csv, os
from matplotlib.pyplot import axis, plot, subplot, setp, gca, show
import matplotlib, sys
#Date format needs to be cleaned
def clean(readfile,writefile):
    hormel = open(readfile,'rU')
    #Preprocessing for single value days i.e. '5-Oct-05' to '05-Oct-05'
    reader = csv.reader(hormel)
    header = reader.next()
    rows = [header]
    for row in reader:
        date = row[0]
        if len(date.split('-')[0])==1:
            row[0] = '0'+date
        rows.append(row)
    writing = open(writefile,"w")
    writer = csv.writer(writing)
    writer.writerows(rows)
    writing.close()

def makeSubplot(fig,number,x, y, yaxis_label, xaxis_label='Open'):
    sp = fig.add_subplot(number)
    plt.scatter(x, y, picker=2)
    sp.set_xlabel(xaxis_label)
    sp.set_ylabel(yaxis_label)
    sp.set_title(yaxis_label,size='x-large',weight='bold')
    sp.xaxis.set_major_locator(MaxNLocator(5))
    return sp

#Making the subplots
#Easy to generalize, just need to tell what datatype
if not os.path.exists('hormel_clean.csv'):
    clean('hormel.csv','hormel_clean.csv')
hormel = open("hormel_clean.csv",'rU')
dateparser = lambda s: datetime.strptime(s, '%d-%b-%y')
dt = np.dtype([('Date', np.object), ('Open', np.float),('High', np.float),('Low', np.float),('Close', np.float),('Volume',np.float)])
hormel_data = np.loadtxt(hormel, dtype=dt,skiprows=1, delimiter=',', converters = {0:dateparser})
dateStr= 'Date'
fig = plt.figure(figsize=(15,10))
#I'm having some problems plotting the date and drawing on the subplots later on
#So I avoid dates

#openprice = makeSubplot(fig,231, hormel_data['Date'],hormel_data['Open'], yaxis_label = 'Open')
#high = makeSubplot(fig,232, hormel_data['Date'],hormel_data['High'], yaxis_label = 'High')
#low = makeSubplot(fig,233, hormel_data['Date'],hormel_data['Low'], yaxis_label = 'Low')
#close = makeSubplot(fig,234, hormel_data['Date'],hormel_data['Close'], yaxis_label = 'Close')
#volume= makeSubplot(fig,235, hormel_data['Date'],hormel_data['Volume'], yaxis_label = 'Volume')

high = makeSubplot(fig,232, hormel_data['Open'],hormel_data['High'], yaxis_label = 'High')
low = makeSubplot(fig,233, hormel_data['Open'],hormel_data['Low'], yaxis_label = 'Low')
close = makeSubplot(fig,234, hormel_data['Open'],hormel_data['Close'], yaxis_label = 'Close')
volume= makeSubplot(fig,235, hormel_data['Open'],hormel_data['Volume'], yaxis_label = 'Volume')

title = fig.add_subplot(236)
title.text(1.05,.5, "Hormel Stock data from Google",ha = "right", va= "top",bbox = dict(boxstyle="square",ec=(1., 0.5, 0.5),fc=(1., 0.8, 0.8),),size='x-large')
title.xaxis.set_major_locator(MaxNLocator(1))
title.yaxis.set_major_locator(MaxNLocator(1))
#canvas = FigureCanvasAgg(fig)
#canvas.print_figure("q3plot.png",dpi=144)
#Starting Event-based handlers
subplots = [high, low, close, volume]


class LineBuilder:
    def __init__(self,plot, line):
        self.line = line
        self.plot = plot
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_key = line.figure.canvas.mpl_connect('key_release_event', self.on_release_key)

    def on_press(self, event):
        print 'click', event
        if event.inaxes!=self.line.axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()
    def on_release_key(self, event):
        if event.key=='d':
            del (self.plot.lines[-1])
            self.linecoord=None
            plt.show()

for subplot in subplots:
    ax = subplot
    line, = ax.plot([0], [0])  # empty line
    linebuilder = LineBuilder(ax,line)

show()
