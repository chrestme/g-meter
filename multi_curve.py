import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import csv

pg.setConfigOptions(antialias=True)

def read_imu_values():
    accX = []
    accY = []
    accZ = []
    gyrX = []
    gyrY = []
    gyrZ = []
    magX = []
    magY = []
    magZ = []
    firstrow = True
    
    with open('/Users/chrestme/BerryIMU/python-LSM9DS0-gryo-accel-compass/test_raw.out') as f:
        imu_reader = csv.reader(f)
        for row in imu_reader:
            if firstrow:
                firstrow = False
                continue
            accX.append(int(row[2]))
            accY.append(int(row[3]))
            accZ.append(int(row[4]))
            
            gyrX.append(int(row[5]))
            gyrY.append(int(row[6]))
            gyrZ.append(int(row[7]))
   
            magX.append(int(row[8]))
            magY.append(int(row[8]))
            magZ.append(int(row[8]))
    
    acc = {'x': accX,
           'y': accY,
           'z': accZ}
    gyr = {'x': gyrX,
           'y': gyrY,
           'z': gyrZ}
    mag = {'x': magX,
           'y': magY,
           'z': magZ}

    return acc,gyr,mag

acc,gyr,mag = read_imu_values()
LA_so = 0.732 #linear accel sensitivity for +/-16G scale 

p1 = pg.plot()
#plot.setAspectLocked()

p1.plot([ (x * LA_so)/1000 for x in acc['x']], pen=(255,0,0), name="Red curve")
p1.plot([ (y * LA_so)/1000 for y in acc['y']], pen=(0,255,0), name="Blue curve")
p1.plot([ (z * LA_so)/1000 for z in acc['z']], pen=(0,0,255), name="Green curve")

#cross hair
vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)
p1.addItem(vLine, ignoreBounds=True)
p1.addItem(hLine, ignoreBounds=True)
label = pg.LabelItem(justify='right')
p1.addItem(label)
vb = p1.getViewBox()

def mouseMoved(evt):
    pos = evt[0]  ## using signal proxy turns original arguments into a tuple
    if p1.sceneBoundingRect().contains(pos):
        mousePoint = vb.mapSceneToView(pos)
        index = int(mousePoint.x())
        if index > 0 and index < len(acc['x']):
            label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>accX=%0.1f</span>,   <span style='color: green'>accY=%0.1f</span>,   <span style='color: blue'>accZ=%0.1f</span>" % (mousePoint.x(), acc['x'][index], acc['y'][index], acc['z'][index]))
        vLine.setPos(mousePoint.x())
        hLine.setPos(mousePoint.y())

proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)

#p2 = pg.plot()
#p2.plot(gyr['x'], pen=(255,0,0), name="Red curve")
#p2.plot(gyr['y'], pen=(0,255,0), name="Blue curve")
#p2.plot(gyr['z'], pen=(0,0,255), name="Green curve")



if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
