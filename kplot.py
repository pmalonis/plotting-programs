"""kplot - an hdf5 data veiwer"""

import numpy as np
import pyqtgraph as pg
import tables
import sys
from PyQt4 import QtGui, QtCore

f = tables.openFile('120820_yy7134_0_0.arf')


def plotAll(f):
    """plot all arrays in file f (code reference)"""
    for g in f.walkGroups():
        print(g)
        for arr in f.listNodes(g, classname='Array'):
            if arr.ndim == 1 and arr.shape[0] > 1:
                pg.plot(arr.read())


def populateTree(f, tree):
    """Currently non-recursive"""
    for group in f.walkGroups():
        topnode = QtGui.QTreeWidgetItem([str(group)])
        topnode.setData(1, 1, group)
        tree.addTopLevelItem(topnode)
        for leaf in f.listNodes(group, classname='Array'):
            lvl2node = QtGui.QTreeWidgetItem([str(leaf)])
            lvl2node.setData(1, 1, leaf)
            topnode.addChild(lvl2node)


def plotData(treeItem, someint):
    print(someint)
    item = treeItem.data(1, 1).toPyObject()
    print(item)
    if type(item) == tables.carray.CArray:
        pg.plot(item.read())
        #atawin.addPlot(row=1, col=0).plot(item.read())


app = QtGui.QApplication(sys.argv)

mainWindow = QtGui.QWidget()
treeview = QtGui.QTreeWidget()
populateTree(f, treeview)
treeview.itemActivated.connect(plotData)
lbl = QtGui.QLabel('stuff')
vbox = QtGui.QVBoxLayout()
vbox.addWidget(treeview)
vbox.addWidget(lbl)
mainWindow.setLayout(vbox)
mainWindow.show()


class MyTree(QtGui.QTreeWidget):
    def __init__(self):
        super(MyTree, self).__init__()

    def sendData(self):
        pass

datawin = pg.GraphicsWindow()
datawin.setWindowTitle('Data Window')
p1 = datawin.addPlot(row=1, col=0)
p2 = datawin.addPlot(row=2, col=0)
p1.plot(f.getNode('/e66225840/yy7134').read())
p2.plot(f.getNode('/e66225840/elec').read())
p1.setXLink(p2)
p1.showGrid(x=True, y=True)
p2.showGrid(x=True, y=True)
sys.exit(app.exec_())
