import sys
from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        qbtn = QtGui.QPushButton('CIAO!', self)
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50,50)

        self.setGeometry(300,300,250,150)
        self.setWindowTitle('APLUOT')
        self.center()
        self.show()

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self,'Message','Are you sure you want to quit?',
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        print 
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
                

def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
