'''
http://wiki.wxpython.org/Getting%20Started ->Best tutorial
http://www.blog.pythonlibrary.org/2010/06/27/wxpython-and-pubsub-a-simple-tutorial/
'''
#!/usr/bin/python
import wx 
wx = wx
import zijderfeldmaker
import paleomag2
import matplotlib
import coreanalysis
import siteanalysis
import math
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

from numpy import arange, sin, pi

    
# Class for creating a page with the graphs and selectors for each core
class CorePage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        pick_text = wx.StaticText(self, -1, "Point Pick")
        pick_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        pick_text.SetSize(pick_text.GetBestSize())
       
        # create a text control and add it to the box
        self.pick_input = wx.TextCtrl(self)
        
        
        
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(pick_text, 0, wx.ALL, 0)
        self.sizer.Add(self.pick_input, 0, wx.ALL, 0)
        
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
         
        '''
         regular zijderfeld here
        '''
        t = arange(0.0, 3.0, 0.01)
        s = sin(pi * t)
        self.axes.plot(t, s)
        
        self.figure2 = Figure()
        self.axes = self.figure2.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure2)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()
        '''
         HC zijderfeld here
        '''
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        self.axes.plot(t, s)
class LatLongPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        lat_text = wx.StaticText(self, -1, "Site lat")
        lat_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        lat_text.SetSize(lat_text.GetBestSize())
        self.lat_input = wx.TextCtrl(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(lat_text, 0, wx.ALL, 0)
        self.sizer.Add(self.lat_input, 0, wx.ALL, 0)    
   
        long_text = wx.StaticText(self, -1, "Site Long")
        long_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        long_text.SetSize(long_text.GetBestSize())
        self.long_input = wx.TextCtrl(self)
        self.sizer.Add(long_text, 0, wx.ALL, 0)
        self.sizer.Add(self.long_input, 0, wx.ALL, 0)    
        
        self.SetSizer(self.sizer)
        self.Fit()
class SiteWindow(wx.Frame):    
    def __init__(self, parent, sites, si, cores, filepath):
        wx.Frame.__init__(self, None, title=sites[si])
        
        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # create the page windows as children of the notebook
        page = CorePage(nb)

        for i in range(0, len(cores)): 
            if sites[si] in filepath[i]: 
        # add the pages to the notebook with the label to show on the tab
                nb.AddPage(page, cores[i])
        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        nb.AddPage(LatLongPage(nb), "Site Info")
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)
        
        


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(750, 100))
        # self.control = wx.TextCtrl(self)
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
        
        # Create Panel in self to put text, then create a 'box' in the panel  
        # panel = wx.Panel(self)
        box = wx.BoxSizer(wx.HORIZONTAL)
        # create some static text and add it to the box
        perc_text = wx.StaticText(self, -1, "Error Percent")
        perc_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        perc_text.SetSize(perc_text.GetBestSize())
        box.Add(perc_text, 0, wx.ALL, 0)
        # create a text control and add it to the box
        self.perc_input = wx.TextCtrl(self)
        box.Add(self.perc_input, 0, wx.ALL, 0)
        
        # create some static text and add it to the box
        angle_text = wx.StaticText(self, -1, "Angle")
        angle_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        angle_text.SetSize(angle_text.GetBestSize())
        box.Add(angle_text, 0, wx.ALL, 0)
        # create a text control and add it to the box
        self.angle_input = wx.TextCtrl(self)
        box.Add(self.angle_input, 0, wx.ALL, 0)
        
        # Adds a check box for basemap
        self.basemap_cb = wx.CheckBox(self, -1, 'Basemap')
        self.basemap_cb.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.basemap_cb.SetSize(angle_text.GetBestSize())
        box.Add(self.basemap_cb, 0, wx.ALL, 0)
        
         
        # Autosize the box and create a layout
        self.SetSizer(box)
        self.Layout()
      
        
        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpenDir, menuOpenDir)

        
        self.Show(True)

    def OnAbout(self, e):
        SiteWindow(frame, 'site').Show()
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(self, "Paleomag", "About Pmag", wx.OK)
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished.

    def OnExit(self, e):
        self.Close(True)  # Close the frame.
        
    def OnOpenDir(self, e):
        """ Open a file"""        
        dlg = wx.DirDialog(self, "Choose a file", "~/", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filesstuff = paleomag2.paleomag2(dlg.GetPath() + '\\')  # gets a few variables from paleomag2
            # all the variables that are passed on to core and site analysis
            sites = filesstuff[0]
            filepath = filesstuff[1]
            textfilename = filesstuff[2]
            cores = filesstuff[3]
            longslist = []  # more lists that need to be made
            latslistr = []  
            dmslist = []
            dpslist = []
            si = 0  
            Dmsitelist = []
            Imsitelist = []   
            for si in range(0, len(sites)):                
                SiteWindow(frame, sites, si, cores, filepath).Show()
                NSSUM = 0
                EWSUM = 0
                UDSUM = 0
                CoreDmslist = []
                CoreImslist = []
                Rlist = []
                coresinsitelist = []  # this doesn't do anything,but I thought it would be useful to have
                N = 0    
                
                for i in range (0, len(filepath)):  # this is the loop that starts each individual file, so once one file is done it goes to the next.
                    asdfs = i
                    # coreanalysis.coreanalysis(si, sites, filepath, i, coresinsitelist, textfilename, float(self.perc_input.GetValue()), cores, math.radians(float(self.angle_input.GetValue())), EWSUM, NSSUM, UDSUM, CoreDmslist, CoreImslist)
                # This is all of the math for the individual sites.Everything should be self explanatory
                # siteanalysis.siteanalysis(sites, si, CoreDmslist, CoreImslist, Dmsitelist, Imsitelist, coresinsitelist, dmslist, latslistr, dpslist, longslist)
           
        dlg.Destroy()    
        
     
    

if __name__ == "__main__":
    app = wx.App()
    frame = MainWindow(None, "Pmag")
    app.MainLoop()
