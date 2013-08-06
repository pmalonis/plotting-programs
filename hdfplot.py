#!/usr/bin/python

"""
hdfplot

a plotting program for hdf5 data
"""

import wx
import wx.lib.plot as plot
import os
import h5py
import numpy as np


class DataPlot(plot.PlotCanvas):
    def __init__(self, parent, id):
        ''' Initialization routine for the this panel.'''
        plot.PlotCanvas.__init__(self, parent, id, style=wx.BORDER_NONE)
        self.update(None)

    def update(self, item):

        if type(item) == h5py._hl.dataset.Dataset:
            data = np.column_stack((np.arange(len(item)), item))
        else:
            data = np.zeros((2, 2))
        line = plot.PolyLine(data)
        graphic = plot.PlotGraphics([line])

        self.Draw(graphic)


class MainGUI(wx.Frame):
    """ The main frame of the application """
    def __init__(self, title="hdfplot", size=(500, 500)):
        super(MainGUI, self).__init__(None,wx.ID_ANY, title, size=size)
        self.dataFile = None
        self.create_menu()
        self.create_toolbar()
        self.create_main_panel()
        self.Centre()
        self.SetAutoLayout(True)
        self.Show(True)

    def create_menu(self):
        fileMenu = wx.Menu()
        openItem = fileMenu.Append(wx.ID_OPEN, '&Open')
        quitItem = fileMenu.Append(wx.ID_CLOSE, '&Quit')

        self.Bind(wx.EVT_MENU, self.on_quit, quitItem)
        self.Bind(wx.EVT_MENU, self.on_open, openItem)

        menubar = wx.MenuBar()
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

    def on_quit(self, event):
        if self.dataFile:
            self.dataFile.close()
        self.Close()

    def on_open(self, event):
        fileDialog = wx.FileDialog(self, "Select a file to open",
                                   style=wx.FD_OPEN)
        val = fileDialog.ShowModal() #shows the dialog
        if val == wx.ID_OK:
            infile = fileDialog.GetPath()
            self.load_file(infile)

    def create_toolbar(self):
        self.toolbar = self.CreateToolBar()

        def ico(x):
           return wx.ArtProvider.GetBitmap(x, wx.ART_TOOLBAR)
        openTool = self.toolbar.AddSimpleTool(wx.ID_ANY, ico(wx.ART_FILE_OPEN),"Open","Open file")
        upTool = self.toolbar.AddSimpleTool(wx.ID_ANY,ico(wx.ART_GO_UP),"Up","Go up")
        downTool = self.toolbar.AddSimpleTool(wx.ID_ANY,ico(wx.ART_GO_DOWN),"Down", "Go Down")
        forwardTool = self.toolbar.AddSimpleTool(wx.ID_ANY,ico(wx.ART_GO_FORWARD),"Forward","Go Forward")
        backTool = self.toolbar.AddSimpleTool(wx.ID_ANY,ico(wx.ART_GO_BACK),"Back","Go Back")
        quitTool = self.toolbar.AddSimpleTool(wx.ID_ANY,ico(wx.ART_QUIT),"Quit","Quit program")
        self.toolbar.Realize()
        self.Bind(wx.EVT_TOOL, self.on_quit, quitTool)
        self.Bind(wx.EVT_TOOL, self.on_open, openTool)

    def create_main_panel(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel1 = wx.Panel(self, wx.ID_ANY)
        panel2 = wx.Panel(self, wx.ID_ANY)
        self.plotCanvas = DataPlot(self, wx.ID_ANY)
        self.tree = wx.TreeCtrl(panel1, 1, wx.DefaultPosition)
        if self.dataFile:
            self.populate_tree()

        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.tree_selection,
                       id=1)
        self.display = wx.StaticText(panel2, wx.ID_ANY,
                                     style=wx.ALIGN_LEFT)
        hbox.Add(self.tree, 1, wx.EXPAND)
        vbox.Add(panel1, 1, wx.EXPAND)
        vbox.Add(panel2, 1, wx.EXPAND)
        panel1.SetSizer(hbox)
        vbox.Add(self.plotCanvas, 1, wx.EXPAND)
        self.SetSizer(vbox)

        """ Status bar """
        self.status = self.CreateStatusBar()
        self.status.SetStatusText('Ready')

    def populate_tree(self):

        def recursive_populate(tree_node, data_node):
            n = self.tree.AppendItem(tree_node, data_node.name)
            self.tree.SetPyData(n,data_node)
            if type(data_node) == h5py._hl.group.Group:
                for i in data_node.values():
                    recursive_populate(n, i)
        '''Add root'''
        data = self.dataFile
        root = self.tree.AddRoot(data.filename)
        self.tree.SetPyData(root,data)
        '''Add rest'''
        for i in data.values():
            recursive_populate(root,i)

    
    def tree_selection(self, event):
        item = self.tree.GetPyData(event.GetItem())
        print(item)
        display_string = ''
        for key, value in item.attrs.items():
            display_string += "%s \t %s \n" %(key,value)
        self.display.SetLabel(display_string)
        self.plot(item)

    def plot(self, item):
        self.plotCanvas.update(item)
            
        
    def load_file(self, infile):
        '''close old data'''
        if self.dataFile:
            self.dataFile.close()
        '''open new data'''
        self.dataFile = h5py.File(infile, 'r')
        self.status.SetStatusText("Opened %s " % infile)
        '''populate tree'''
        self.populate_tree()


def main():
    app = wx.App()
    MainGUI()
    app.MainLoop()

if __name__ == '__main__':
    main()
