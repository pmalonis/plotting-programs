import wx
from matplotlib.figure import Figure
import numpy as np
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigureCanvas

class MplCanvasFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          title='Matplotlib in Wx', size=(600, 400))
        #super(MplCanvasFrame, self).__init__(self, None, wx.ID_ANY)
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.axes = self.figure.add_subplot(111)
        x = np.arange(0, 6, 0.1)
        y = x**2
        self.axes.plot(x,y)
        self.canvas = FigureCanvas(self, wx.ID_ANY, self.figure)

app = wx.App()
frame = MplCanvasFrame()   
frame.Show(True)
app.MainLoop()
