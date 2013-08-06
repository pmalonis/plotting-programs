import sys
from PyQt4 import QtGui

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.initUI()

    def initUI(self):
        textEdit = QtGui.QTextEdit()
        #self.setCent
    
        exitAction = QtGui.QAction(QtGui.QIcon.fromTheme('exit'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
        saveAction = QtGui.QAction(QtGui.QIcon.fromTheme('document-save'), '&Save',self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(QtGui.qApp.quit)
        saveAction.setStatusTip('Save to disk')

        self.statusBar().showMessage('Ready')
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(saveAction)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(saveAction)
        
        
        self.setGeometry(300,300,250,150)
        self.setWindowTitle('AWESOMEbar')
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    
