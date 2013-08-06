import wx

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MainFrame,self).__init__(*args,**kwargs)
        self.InitUI()
        

    def InitUI(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_EXIT,'Quit','Quit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)

        self.SetSize((300,200))
        self.SetTitle('Simple menu')
        
        self.Centre()
        self.Show()

    def OnQuit(self, e):
        self.Close()

    
if __name__=='__main__':
    app = wx.App()
    MainFrame(None)
    app.MainLoop()
