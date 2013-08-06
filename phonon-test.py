import sys
from PyQt4 import QtCore
from PyQt4.phonon import Phonon

app = QtCore.QCoreApplication(sys.argv)
app.setApplicationName("my_player")
# phonon useage requires an application name

m = Phonon.MediaSource("temp.wav")
obj = Phonon.createPlayer(Phonon.MusicCategory, m)
obj.play()

app.exec_()
