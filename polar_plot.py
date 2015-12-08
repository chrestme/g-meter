import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np

#QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])
#mw = QtGui.QMainWindow()
#mw.resize(800,800)

win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')


# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)
p1 = win.addPlot(title="Polar Plot")
#plot = pg.plot(pen='y')
#plot.setAspectLocked()

# Add polar grid lines
p1.addLine(x=0, pen=0.2)
p1.addLine(y=0, pen=0.2)
for r in range(0, 2, 1):
    circle = pg.QtGui.QGraphicsEllipseItem(-r, -r, r*2, r*2)
    circle.setPen(pg.mkPen(0.2))
    p1.addItem(circle)

            # make polar data
#theta = np.linspace(0,np.pi,100)    #[0,np.pi/4]    #np.linspace(0, 2*np.pi, 100)
#radius = 10        #np.random.normal(loc=10, size=100)

# Transform to cartesiani and plot
#x = radius * np.cos(theta)
#y = radius * np.sin(theta)

import csv
with open('test_raw.out') as f:
    imu_data = csv.reader(f)
    first_row = True
    x = []
    y = []
    for row in imu_data:
        if first_row:
            first_row = False
            continue

        x.append((int(row[2]) * .762)/1000)
        y.append((int(row[3]) * .762)/1000)

p1.plot(x, y)

import math
p2 = win.addPlot()
s1 = pg.ScatterPlotItem(pxMode = True) #size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 20))
spots = []
ptr = 0
#for i in range(len(x)):
def update():
    global s1,x,y,p2,ptr
    s1.clear()
    if ptr == 0:
        p2.enableAutoRange('xy', False)
    spots = [{'pos': (x[ptr], y[ptr]), 'size': 1, 'pen': {'color': 'w', 'width': 6}, 'brush':pg.mkBrush(255, 255, 0, 100)}]
    s1.addPoints(spots)
    p2.addItem(s1)
    ptr += 1
#s4.sigClicked.connect(clicked)


#curve = p6.plot(pen='y')
#data = np.random.normal(size=(10,1000))
#ptr = 0
#def update():
#    global curve, data, ptr, plot
#while ptr < 100:
#    plot.setData(radius * np.cos(theta[ptr]),radius * np.sin(theta[ptr]))
#        if ptr == 0:
#            plot.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
#        ptr += 1

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(38)

if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
