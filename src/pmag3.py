'''
I had an idea 
it was...
put the max error and the angle on the main screen in panels.
then create tabs for the site core
then have sliders that do all of the graphing based on core parms of "select this point"
also maybe have a universal select.
At the end have a checkbox pop up with everything that we want as output e.g. core pdf graphs and text
maybe a window per core instead of tabs
This is about the event driven structure instead of the sequential which we've got now
Talk to scott. 

'''
import wx
import paleomag2

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200, 100))
        self.control = wx.TextCtrl(self)
        self.CreateStatusBar()  # A StatusBar in the bottom of the window

        # Setting up the menu.
        filemenu = wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")
        menuOpenDir = filemenu.Append(wx.ID_OPEN, "OpenDir", "Opens a file")

        # Creating the menubar.
        
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")  # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpenDir, menuOpenDir)


        self.Show(True)

    def OnAbout(self, e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(self, "A small text editor", "About Sample Editor", wx.OK)
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished.

    def OnExit(self, e):
        self.Close(True)  # Close the frame.
        
    def OnOpenDir(self, e):
        """ Open a file"""
        
        dlg = wx.DirDialog(self, "Choose a file", "~/", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            
            self.control.SetValue(dlg.GetPath())
            paleomag2.paleomag2(dlg.GetPath() + '\\')
        dlg.Destroy()    
    
app = wx.App()  # put htis to wx.App(0) to send everything to console

frame = MainWindow(None, "Pmag")
app.MainLoop()
