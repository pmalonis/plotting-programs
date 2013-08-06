import sys
from PySide import QtGui
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg \
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg \
    import NavigationToolbar2QTAgg as MPLToolbar

class Qt4MplCanvas(FigureCanvas):
    def __init__(self, parent):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        self.x = np.arange(0, 10e3)
        self.y = np.cos(self.x/100)
        self.axes.plot(self.x, self.y)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.setWindowTitle("Matplotlib in PySide")
        self.main_widget = QtGui.QWidget(self)
        vbl = QtGui.QVBoxLayout(self.main_widget)
        qmc = Qt4MplCanvas(self.main_widget)
        ntb = MPLToolbar(qmc, self.main_widget)
        vbl.addWidget(qmc)
        vbl.addWidget(ntb)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

qApp = QtGui.QApplication(sys.argv)
mpl = ApplicationWindow()
mpl.show()
sys.exit(qApp.exec_())















