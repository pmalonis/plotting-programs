from __future__ import division
import traits.api
import traitsui.api
from enable.api import ColorTrait
from enable.component_editor import ComponentEditor
import chaco.api
import chaco.tools.api
import numpy as np

class ScatterPlotTraits(traits.api.HasTraits):

    plot = traits.api.Instance(chaco.api.Plot)
    color = ColorTrait("blue")
    marker = chaco.api.marker_trait
    marker_size = traits.api.Int(4)

    traits_view = traitsui.api.View(
        traitsui.api.Group(traitsui.api.Item('color', label="Color", style="custom"),
                           traitsui.api.Item('marker', label="Marker"),
                           traitsui.api.Item('marker_size', label='Size'),
                           traitsui.api.Item('plot', editor=ComponentEditor()),
                           orientation="vertical"),
        width=800, height=600, resizable=True, title="Ye olde plot")

    def __init__(self):
        super(ScatterPlotTraits, self).__init__()
        x = np.arange(100)
        y = np.sin(x / 40)
        plotdata = chaco.api.ArrayPlotData(x=x, y=y)
        plot = chaco.api.Plot(plotdata)

        # append tools to pan, zoom, and drag
        plot.tools.append(chaco.tools.api.PanTool(plot))
        plot.tools.append(chaco.tools.api.ZoomTool(plot))
        plot.tools.append(chaco.tools.api.DragZoom(plot, drag_button="right"))

        self.renderer = plot.plot(("x", "y"), type="scatter", color="blue")[0]
        self.plot = plot
        
        

    def _color_changed(self):
        self.renderer.color = self.color

    def _marker_changed(self):
        self.renderer.marker = self.marker

    def _marker_size_changed(self):
        self.renderer.marker_size = self.marker_size

if __name__ == '__main__':
    ScatterPlotTraits().configure_traits()




















