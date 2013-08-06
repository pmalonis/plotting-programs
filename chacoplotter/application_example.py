from traits.api import HasTraits, Instance
from traitsui.api import View, Item
from chaco.api import Plot, ArrayPlotData
from enable.component_editor import ComponentEditor
from numpy import linspace, exp, meshgrid, sin, cos
import numpy as np


class LinePlot(HasTraits):
    plot = Instance(Plot)

    traits_view = View(
        Item('plot', editor=ComponentEditor(), show_label=True),
        width=500, height=500, resizable=True, title="Chaco! Plot")

    def __init__(self):
        super(LinePlot, self).__init__()
        x = linspace(-14, 14, 100)
        y = np.sin(x) * x**3
        y2 = np.sin(x) * 1000
        plotdata = ArrayPlotData(x=x, y=y, y2=y2)

        plot = Plot(plotdata)
        #plot.img_plot("imagedata")
        plot.plot(("x", "y"), type="line", color="grey")
        plot.plot(("x", "y2"), type="scatter", color="red")
        plot.title = "It's a thing I plotted"

        self.plot = plot
'''
if __name__ == "__main__":
    LinePlot().configure_traits()

'''


class OverlappingPlot(HasTraits):

    plot = Instance(Plot)

    traits_view = View(
        Item('plot', editor=ComponentEditor(), show_label=False),
        width=500, height=500, resizable=True, title="Chaco Plot")

    def __init__(self):
        super(OverlappingPlot, self).__init__()

        x = linspace(-14, 14, 100)
        y = x/2 * sin(x)
        y2 = cos(x)
        plotdata = ArrayPlotData(x=x, y=y, y2=y2)

        plot = Plot(plotdata)
        plot.plot(("x", "y"), type="scatter", color="blue")
        plot.plot(("x", "y2"), type="line", color="red")

        self.plot = plot

if __name__ == "__main__":
    LinePlot().configure_traits()

