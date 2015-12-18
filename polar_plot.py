import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np

app = QtGui.QApplication([])

win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(800,800)
win.setWindowTitle('pyqtgraph example: Plotting')


pg.setConfigOptions(antialias=True)

for r in range(0, 2, 1):
    circle = pg.QtGui.QGraphicsEllipseItem(-r, -r, r*2, r*2)
    circle.setPen(pg.mkPen(0.2))

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

import math
p2 = win.addPlot()
p2.addLine(x=0, pen=0.2)
p2.addLine(y=0, pen=0.2)
p2.addItem(circle)
s1 = pg.ScatterPlotItem(pxMode = True) #size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 20))
spots = []
ptr = 0

def update():
    global s1,x,y,p2,ptr
    s1.clear()
    if ptr == 0:
        p2.enableAutoRange('xy', False)
    spots = [{'pos': (x[ptr], y[ptr]), 'size': 2, 'pen': {'color': 'w', 'width': 10}, 'brush': pg.mkBrush(255, 255, 0, 100)}]
    s1.addPoints(spots)
    p2.addItem(s1)
    ptr += 1

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(38)

if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
