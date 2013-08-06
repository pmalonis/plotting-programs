"""an alpha version of the plotter"""

from __future__ import absolute_import, division, \
    print_function, unicode_literals
from PySide import QtGui, QtCore
import signal
import sys
import pyqtgraph as pg
import pyqtgraph.dockarea as pgd
import h5py
import numpy as np
import os
#from PyQt4.phonon import Phonon
from matplotlib.mlab import specgram
from scipy.io import wavfile


class MainWindow(QtGui.QMainWindow):
    '''the main window of the program'''
    def __init__(self):
        super(MainWindow, self).__init__()
        self.current_file = None
        self.initUI()

    def initUI(self):
        """"Assembles the basic Gui layout, status bar, menubar
        toolbar etc."""
        # status bar
        self.statusBar().showMessage('Ready')

        # actions
        soundAction = QtGui.QAction(QtGui.QIcon('icons/sound.svg'),
                                    'PlaySound', self)
        soundAction.setShortcut('Ctrl+S')
        soundAction.setStatusTip('Play data as sound')
        soundAction.triggered.connect(self.playSound)
        exitAction = QtGui.\
            QAction(QtGui.QIcon('icons/system-shutdown-panel.svg'),
                    'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
        openAction = QtGui.\
            QAction(QtGui.QIcon('icons/document-open.svg'), 'Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open an arf file')
        openAction.triggered.connect(self.showDialog)
        # menubar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(openAction)

        # toolbar
        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(openAction)
        self.toolbar.addAction(soundAction)

        # file tree
        self.tree_view = QtGui.QTreeWidget()
        self.tree_view.currentItemChanged.connect(self.plotData)
        if self.current_file:
            self.populateTree()

        #attribute table
        self.attr_table = QtGui.QTableWidget(10, 2)

        #plot region
        self.data_layout = pg.GraphicsLayoutWidget()

        # final steps
        self.area = pgd.DockArea()
        tree_dock = pgd.Dock("Tree", size=(1, 1))
        data_dock = pgd.Dock("Data", size=(500, 200))
        attr_table_dock = pgd.Dock("Attributes", size=(1, 1))
        self.area.addDock(tree_dock, 'left')
        self.area.addDock(data_dock, 'right')
        self.area.addDock(attr_table_dock, 'bottom', tree_dock)
        tree_dock.addWidget(self.tree_view)
        data_dock.addWidget(self.data_layout)
        attr_table_dock.addWidget(self.attr_table)
        self.setCentralWidget(self.area)
        self.setWindowTitle('ooplot')
        self.resize(1000, 500)
        self.show()

    def showDialog(self):
        fname = QtGui.QFileDialog.\
            getOpenFileName(self, 'Open file', '.',
                            '*.arf ;; *.hdf5, *.h5 ;; *.mat')
        print("%s opened" % (fname))
        self.statusBar().showMessage("%s opened" % (fname))
        self.current_file = h5py.File(str(fname))
        self.populateTree()

    def populateTree(self):
        f = self.current_file

        def recursivePopulateTree(parent_node, data):
            tree_node = QtGui.QTreeWidgetItem([data.name])
            tree_node.setData(0, QtCore.Qt.UserRole, data)
            parent_node.addChild(tree_node)
            if type(data) == h5py._hl.group.Group:
                for item in data.itervalues():
                    recursivePopulateTree(tree_node, item)

        # add root
        topnode = QtGui.QTreeWidgetItem([f.filename])
        root = f["/"]
        topnode.setData(0, QtCore.Qt.UserRole, root)
        self.tree_view.addTopLevelItem(topnode)
        for item in root.itervalues():
            recursivePopulateTree(topnode, item)

    def plotDataset(self, dataset, irow, kind='osc'):
        #datatype = dataset.attrs['datatype']
        sr = float(dataset.attrs['sampling_rate'])
        t = np.arange(0, len(dataset)) / sr
        if kind == 'osc':
            pl = self.data_layout.addPlot(title=dataset.name,
                                          name=str(irow), row=irow, col=0)
            pl.plot(t, dataset)
            pl.showGrid(x=True, y=True)
            #pl.Dow
        if kind == 'spec':
            Pxx, freqs, ts = specgram(dataset, Fs=sr, NFFT=512, noverlap=400)
            img = pg.ImageItem(np.log(Pxx.T))
            #img.setLevels((-5, 10))
            img.setScale(ts[-1] / Pxx.shape[1])
            vb = self.data_layout.addViewBox(name=str(irow), row=irow, col=0)
            g = pg.GridItem()
            vb.addItem(g)
            vb.addItem(img)
            vb.setMouseEnabled(x=True, y=False)
            return vb, img

        return pl

    def plotData(self, treeItem):
        item = treeItem.data(0, QtCore.Qt.UserRole).toPyObject()
        populateAttrTable(self.attr_table, item)
        self.data_layout.clear()
        self.masterYLink = None
        if type(item) == h5py._hl.group.Group:
            for i, node in enumerate(item.itervalues()):
                if canPlot(node) and \
                   'trig_in' not in node.name:
                    # assume first entry is acoustic
                    #if node.attrs['datatype'] in [1]:  # acoustic
                    if i == 0:
                        # plot both oscilogram and spectrogram
                        song_spec_vb, song_spec_img = \
                            self.plotDataset(node, 0, kind='spec')
                        song_osc = self.plotDataset(node, 1, kind='osc')
                        self.masterXLink = song_osc
                        song_spec_vb.setXLink(self.masterXLink)
                    else:
                        n_osc = self.plotDataset(node, i+1, kind='osc')
                        n_osc.setXLink(song_osc)
            ''''
            for node in item.itervalues():
                i = 2  # collumn for plot
                if canPlot(node):
                    if node.attrs['datatype'] in [0, 2]:  # neural
                        # plot both oscilogram and spectrogram
                        n_osc = self.plotDataset(node, i, kind='osc')
                        i += 1
                        if self.masterXLink:
                            n_osc.setXLink(song_osc)
            '''
        elif canPlot(item):
            self.plotDataset(item, 0)

#    def playSound(self):
#        pass

    def playSound(self):
        data = self.tree_view.currentItem()\
            .data(0, QtCore.Qt.UserRole).toPyObject()
        print('writing wav file')
        if canPlot(data):
            wavfile.write('temp.wav', data.attrs['sampling_rate'],
                          np.array(data))
            os.system('totem temp.wav')

            '''
            if QtGui.QSound.isAvailable():
                QtGui.QSound.play('temp.wav')
            else:
                from soundplayer import SoundWindow
                #soundapp = QtGui.QApplication([])
                #soundapp.setApplicationName('Phonon')
                win = SoundWindow()
                win.show()
                #sys.exit(soundapp.exec_())
                print('trying Phonon')
                m = Phonon.MediaSource("temp.wav")
                obj = Phonon.createPlayer(Phonon.MusicCategory, m)
                obj.play()
                print(obj)
                #source = Phonon.MediaSource("temp.wav")
                #player = Phonon.createPlayer(Phonon.MusicCategory, source)
                #player.play()
        print('playSound done')
#            music = pyglet.resource.media('temp.wav')
#            music.play()
#            pyglet.app.run()
#           sound = QtGui.QSound('temp.wav')
#            sound.play()
#            output = Phonon.AudioOutput(Phonon.MusicCategory)
#            m_media = Phonon.MediaObject()
#            Phonon.createPath(m_media, output)
#            m_media.setCurrentSource(Phonon.MediaSource("temp.wav"))
#            m_media.play()

'''
def playSound(data):
    print('writing wav file')
    if canPlot(data):
        wavfile.write('temp.wav', data.attrs['sampling_rate'],
                      np.array(data))
        os.system('totem temp.wav')

def populateAttrTable(table, item):
    """Populate QTableWidget with attribute values of hdf5 item ITEM"""
    table.setRowCount(len(item.attrs.keys()))

    for row, (key, value) in enumerate(item.attrs.iteritems()):
        attribute = QtGui.QTableWidgetItem(str(key))
        attribute_value = QtGui.QTableWidgetItem(str(value))
        table.setItem(row, 0, attribute)
        table.setItem(row, 1, attribute_value)


def canPlot(dataset):
    try:
        iter(dataset)
        if len(dataset) > 0 and 'datatype' in dataset.attrs.keys():
            return True
    except TypeError:
        print(dataset, ' is not iterable')
    return False


def sigint_handler(*args):
    """Handler for the SIGINT signal."""
    sys.stderr.write('\r')
    QtGui.QApplication.quit()


def main():
    signal.signal(signal.SIGINT, sigint_handler)
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('ooplot')
    timer = QtCore.QTimer()
    timer.start(500)  # You may change this if you wish.
    timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.
    mainWin = MainWindow()
    sys.exit(app.exec_())
    #if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    #    QtGui.QApplication.instance().exec_()
if __name__ == '__main__':
    main()
