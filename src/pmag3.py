'''
http://wiki.wxpython.org/Getting%20Started ->Best tutorial
http://www.blog.pythonlibrary.org/2010/06/27/wxpython-and-pubsub-a-simple-tutorial/
'''
#!/usr/bin/python
import wx 
wx = wx
import paleomag2
import matplotlib
matplotlib.use('WXAgg')
import linecache
import math
import pdfcreator
from wx.lib.pubsub import Publisher

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure


    
# Class for creating a page with the graphs and selectors for each core
class CorePage(wx.Panel):
    def __init__(self, parent, filepath, i, textfilename, maxerror, maxangler):
        wx.Panel.__init__(self, parent, size=(800, 640))
        pick_text = wx.StaticText(self, -1, "Point Pick")
        pick_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        pick_text.SetSize(pick_text.GetBestSize())

       
        # create a text control and add it to the box
        self.pick_input = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)        
        
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(pick_text, 0, wx.ALL, 0)
        self.sizer.Add(self.pick_input, 0, wx.ALL, 0)
        
        
         
        '''
         regular zijderfeld here
        '''

        # Core Analysis segments
        datafile = open(filepath[i])  # open is used to put a file into memory so it can be read/written to.
        # Finds total number of lines in file
        # coresinsitelist.append(filepath[i])
        linestotal = len(datafile.readlines())  # len() gets the length of a list and file.readlines() returns a list of lines in the file, whose length would be the number of lines
    
        # Puts relevant lines into a lists. For example, lines2list are all of the lines that are
        # like line 2, which give sample name demag step and date.These would be lines 2, 24,46...22n+2.
        # There is always a separation of 22 lines from one test to another, hopefully, since
        # that is the basis for this script to work
    
        n = 0  # assigns a variable that I used for counting in loops
        lines2list = []  # creates a list with no elements that we will fill with a loop
        for n in range(1, linestotal):  # this loop fills the list. The first condition here tells it when to start and stop
            if n == 2:  # The first line of its time
                lines2list.append(linecache.getline(filepath[i], n))  # file.append() adds an element to the end of a list. linecache.getline() takes the specified line in the specified file. The loop is constructed so n is the same as the line number it is on
    
            if ((n - 2) % 22) == 0:  # If the remainder is 0, then write the line.
                lines2list.append(linecache.getline(filepath[i], n))
    
            else:  # adds one to n to test the next line.
                n = n + 1
        # commented this out because we only need lines 2, 14 and 19 of the txtfile
        lines13list = []
        for n in range(1, linestotal):
            if n == 13:
                lines13list.append(linecache.getline(filepath[i][i], n))
    
            if ((n - 13) % 22) == 0:
                lines13list.append(linecache.getline(filepath[i], n))
            else:
                n = n + 1
        lines14list = []
        for n in range(1, linestotal):
                if n == 14:
                    lines14list.append(linecache.getline(filepath[i], n))
            
                if ((n - 14) % 22) == 0:
                    lines14list.append(linecache.getline(filepath[i], n))
                else:
                    n = n + 1
        lines19list = []
        for n in range(1, linestotal):
            if n == 19:
                lines19list.append(linecache.getline(filepath[i], n))
        
            if ((n - 19) % 22) == 0:
                lines19list.append(linecache.getline(filepath[i], n))
            else:
                n = n + 1
        # gets number of data points which is also the number of demagsteps (any of the above looped lists would have worked.)
        numdemagsteps = len(lines2list)
        n = 0
        # This section will split the lists into their needed components
        # and then will write the file line by line in a loop
        
        writefilename = textfilename[i].rstrip("txt") + "dmg"  # creates our filename. It just replaces the .txt with dmg, which I have kept doing to differentiate the two textfiles.
        outputdmg = open(writefilename, "w")  # opens a file named <samplename>.dmg for writing
        columnlabels = ["Sample_Name", " ", "Demag_Step", " ", "Total_Magnitude", " ", "X_avg", " ", "Y_avg", " ", "Z_avg", " ", "Declination", " ", "Inclination", " ", "Date", ' ', "Error", "\n"]  # a list I made of column labels in order to make things more explanatory
        outputdmg.writelines(columnlabels)  # writes the column lables as the first line of the .dmg file. Put a '#' in front of this line to turn it off. <file>.writelines() writes a line that is the argument, in this case a list
        inclination = []
        declination = []
        magnitude = []
        demagsteps = []
        for n in range(1, numdemagsteps):
            splitlines14 = lines14list[n].split()
            # each of the linesXlist are a     list with each element as an entire line of text. This takes an individual element of that list (a line) and breaks it up into its components and puts it in a list, in this case ['Modulus',' '.'2.309E-03',' ','A/m',' ','Prec',' ','1.2',' ','0.7%']
            splitlines19 = lines19list[n].split()        
            splitlines2 = lines2list[n].split()
            splitlines13 = lines13list[n].split() 
            demagsteps.append(splitlines2[2])
            # file without space on line 14 (old file type)
            if 'E' in splitlines14[2]:
                # separates out the two digit and one digit precision problem
                if len(splitlines14) == 6:
                    oneline = [splitlines2[0], " ", splitlines2[2], " ", splitlines14[1] + splitlines14[2].strip('A/m'), " ", splitlines13[1], " ", splitlines13[2], " ", splitlines13[3], " ", splitlines19[1], " ", splitlines19[2], " ", splitlines2[3], " ", splitlines14[5], "\n"]  # Makes a list that is composed of the wanted elements of each of the lines.
                    if float(splitlines14[5].strip('%')) < maxerror:
                        outputdmg.writelines(oneline)  # writes the lines
                        declination.append(splitlines19[1])
                        inclination.append(splitlines19[2])
                        magnitude.append(splitlines14[1] + splitlines14[2].strip('A/m'))
                if len(splitlines14) == 5: 
                    oneline = [splitlines2[0], " ", splitlines2[2], " ", splitlines14[1] + splitlines14[2].strip('A/m'), " ", splitlines13[1], " ", splitlines13[2], " ", splitlines13[3], " ", splitlines19[1], " ", splitlines19[2], " ", splitlines2[3], " ", splitlines14[4], "\n"]  # Makes a list that is composed of the wanted elements of each of the lines.
                    if float(splitlines14[4].strip('%')) < maxerror:
                        outputdmg.writelines(oneline)  # writes the lines
                        declination.append(splitlines19[1])
                        inclination.append(splitlines19[2])
                        magnitude.append(splitlines14[1] + splitlines14[2].strip('A/m'))
                
            
            # files with space on line 14 (new file type)
            if 'E' in splitlines14[1]:
                if len(splitlines14) == 6:
                    oneline = [splitlines2[0], " ", splitlines2[2], " ", splitlines14[1], " ", splitlines13[1], " ", splitlines13[2], " ", splitlines13[3], " ", splitlines19[1], " ", splitlines19[2], " ", splitlines2[3], " ", splitlines14[5], "\n"]  # Makes a list that is composed of the wanted elements of each of the lines.
                               
                    if float(splitlines14[5].strip("%")) < maxerror:
                        outputdmg.writelines(oneline)  # writes the lines
                        declination.append(splitlines19[1])
                        inclination.append(splitlines19[2])
                        magnitude.append(splitlines14[1])  
                if len(splitlines14) == 5:
                    oneline = [splitlines2[0], " ", splitlines2[2], " ", splitlines14[1], " ", splitlines13[1], " ", splitlines13[2], " ", splitlines13[3], " ", splitlines19[1], " ", splitlines19[2], " ", splitlines2[3], " ", splitlines14[4], "\n"]  # Makes a list that is composed of the wanted elements of each of the lines.
                    if float(splitlines14[4].strip("%")) < maxerror:
                        outputdmg.writelines(oneline)  # writes the lines
                        declination.append(splitlines19[1])
                        inclination.append(splitlines19[2])
                        magnitude.append(splitlines14[1])  
            # outputdmg.writelines(linevar[n-2])
            n = n + 1
         
        # This section starts the math for each individual core    
        ns = []  # These lists will hold info specific to a core. After going out of the loop their info will be gone
        ew = []
        ud = []
        for n in range (0, len(inclination)):  # loop does the math to take inclinations and declinations and turn them into core ns, ew, ud
                    incrad = math.radians(float(inclination[n]))                
                    decrad = math.radians(float(declination[n]))                 
                    mag = float(magnitude[n]) 
                    ns.append(mag * math.cos(decrad) * math.cos(incrad))
                    ew.append(mag * math.cos(incrad) * math.sin(decrad))
                    ud.append(mag * math.sin(incrad))
        declination = [float(foo) for foo in declination]
        inclination = [float(foo) for foo in inclination]
        # makes plots
        negew = []  # zeiderfeld plots use negative axis 
        negud = []
        for n in range(0, len(ew)):
            negew.append(-1 * ew[n])
            negud.append(-1 * ud[n])     
        labels = ['{0}'.format(foo) for foo in range(len(ns))]
            
        ########################################################
        # wx part for Zijderfeld(full)   
            
        # Note: do not use i any more!
        
        # Regression section for simulated/suggested high coercivity pick.
         
        thetalistew = []  # will hold angles
        thetalistud = []
        # gets slopes of one ns/ew line
      
        for n in range(1, len(ns)):
            m = math.atan2((negew[n] - negew[n - 1]), (ns[n] - ns[n - 1]))        
            thetalistew.append(m)
        for n in range(1, len(ns)):
            m = math.atan2((negud[n] - negud[n - 1]), (ns[n] - ns[n - 1]))         
            thetalistud.append(m)     
        
       
        n = 0       
        ewc = []
        udc = []
        
        
        # print 'There are ' + str(len(thetalistew)) + ' slope segments steps for this core'
        # print 'Enter the number of the segments you want to use'
        # pylab.show(block=False)
        # lng = input()  

        self.axes.plot(ns, negew, "-o", label='ns vs negew') + self.axes.plot(ns, negud, "-o", label='ns vs negud')
        
        for label, x, y in zip(labels, ns, negew):
            self.axes.annotate(
                label,
                xy=(x, y), xytext=(0, 10),
                textcoords='offset points', ha='right', va='bottom')
        for label, x, y in zip(labels, ns, negud):
            self.axes.annotate(
                label,
                xy=(x, y), xytext=(0, 10),
                textcoords='offset points', ha='right', va='bottom') 
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        
        self.figure2 = Figure()
        self.axes = self.figure2.add_subplot(111)
        self.canvas2 = FigureCanvas(self, -1, self.figure2)
        self.sizer.Add(self.canvas2, 1, wx.LEFT | wx.BOTTOM | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()
        '''
        Dynamic graph part
        '''
        # creates event to call hcplot
        self.Bind(wx.EVT_TEXT, lambda event: self.hcplot(event, thetalistew, maxangler, thetalistud, ewc, udc, ns, negew, negud), self.pick_input)
    
    def hcplot(self, event, thetalistew, maxangler, thetalistud, ewc, udc, ns, negew, negud):
        
        
        if (self.pick_input.GetValue() == ""):
            lng = 0
        elif(int(self.pick_input.GetValue()) > len(ns)):
            
            lng = len(ns) - 1
        else:
            lng = int(self.pick_input.GetValue())
        for n in range(0, lng):  # basically, compares the slopes of the lines to see if they are similar. Puts a 1 if similar and 0 if not 
            cp = []
            cp2 = []
            for m in range(0, lng):
                if thetalistew[n] - maxangler < thetalistew[m] < maxangler + thetalistew[n]:
                    cp.append(1)  
                else: 
                    cp.append(0)
            for m in range(0, lng):
                if thetalistud[n] - maxangler < thetalistud[m] < maxangler + thetalistud[n]:
                    cp2.append(1)  
                else: 
                    cp2.append(0)               
            ewc.append(cp)  # appends the cp (and cp2) lists to another list, making a list of list of slopes
            udc.append(cp2)
        udcsum = 0
        ewcsum = 0
        
        for n in range(0, len(udc[-1])):  # counts the number of 1's in each of the coercivity pick lists
            udcsum = udcsum + udc[-1][n]
            ewcsum = ewcsum + ewc[-1][n]
        hcoproto = []
        if udcsum > ewcsum:  # this if/else picks determines if the ew or ud coercivity pick is better by picking the one with the least 1s in it
            hcoproto = ewc[-1]
        else:
            hcoproto = udc[-1]
        hcoproto.reverse()  # flips the list order
        hcoercepicks = [1]  # This makes the last pick always part of the high coercivity component.
        
        
        for n in range(0, len(hcoproto)):  # This fills the list properly, with 0s and then 1s for the high coercivity part
            if hcoproto[n] == 1:  # just keeps adding 1's until there are none left in hcoproto
                hcoercepicks.append(1)
            else:  # fills in the rest with 0s
                foo = [0] * (len(hcoproto) - n)
                for j in range(0, len(foo)):
                    hcoercepicks.append(foo[j])
                break    
        
        hcoercepicks.reverse()
        # Creates a graph of the high coercivity park based on the hcoercepicks list, same as above
        nshcoerce = []
        negewhcoerce = []
        negudhcoerce = []
        n = 0
        for n in range(0, len(hcoercepicks)):
            if hcoercepicks[n] == 1:
                nshcoerce.append(ns[n])
                negewhcoerce.append(negew[n])
                negudhcoerce.append(negud[n])
        self.axes.clear()
        self.axes.plot(nshcoerce, negewhcoerce, "-o", label='ns vs negew') + self.axes.plot(nshcoerce, negudhcoerce, "-o", label='ns vs negud')
        labels = [str(foo + lng - len(nshcoerce) + 1) for foo in range(len(ns))]
        for label, x, y in zip(labels, nshcoerce, negewhcoerce):
            self.axes.annotate(
                label,
                xy=(x, y), xytext=(0, 10),
                textcoords='offset points', ha='right', va='bottom')
        for label, x, y in zip(labels, nshcoerce, negudhcoerce):
            self.axes.annotate(
                label,
                xy=(x, y), xytext=(0, 10),
                textcoords='offset points', ha='right', va='bottom') 
        self.canvas2.draw()
    
            
class LatLongPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        lat_text = wx.StaticText(self, -1, "Site lat")
        lat_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        lat_text.SetSize(lat_text.GetBestSize())
        
        self.lat_input = wx.TextCtrl(self)
        
        long_text = wx.StaticText(self, -1, "Site Long")
        long_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        long_text.SetSize(long_text.GetBestSize())
        
        self.long_input = wx.TextCtrl(self)
        
        closeBtn = wx.Button(self, label="Send and Close")
        closeBtn.Bind(wx.EVT_BUTTON, self.onSendAndClose)
          
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(lat_text, 0, wx.ALL, 0)
        self.sizer.Add(self.lat_input, 0, wx.ALL, 0)    
        self.sizer.Add(closeBtn, 0, 5)
        self.sizer.Add(long_text, 0, wx.ALL, 0)
        self.sizer.Add(self.long_input, 0, wx.ALL, 0)    
        
        self.SetSizer(self.sizer)
        self.Fit()
     
        
    def onSendAndClose(self, event):
        latinput = self.lat_input.GetValue()
        longinput = self.lat_input.GetValue()
        latlong = [latinput, longinput]
        Publisher().sendMessage(("givelatlong"), latlong)
        self.GrandParent.Parent.Destroy()
class SiteWindow(wx.Frame):    
    def __init__(self, parent, sites, si, cores, filepath, textfilename, maxerror, maxangler, dirpath):
        wx.Frame.__init__(self, None, title=sites[si], size=(800, 640))
        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)
        
        # create the page windows as children of the notebook
       

        for i in range(0, len(cores)):          
            if sites[si] in filepath[i]: 
        # add the pages to the notebook with the label to show on the tab
                pdfcreator.pdfcreator(si, sites, filepath, i, textfilename, maxerror, cores, maxangler, dirpath)
                nb.AddPage(CorePage(nb, filepath, i, textfilename, maxerror, maxangler), cores[i])
        #######################################################################
        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        nb.AddPage(LatLongPage(nb), "Site Info")
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)
        
'''  
class MainPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
 
        
        # print reciever
        # self.pubsubText = wx.TextCtrl(self, value="")
        
        # print(self.pubsubText)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.pubsubText, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(sizer)
 
        # self.pubsubText.SetValue(msg.data)
'''

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
        self.perc_input = wx.TextCtrl(self, value='5')
        box.Add(self.perc_input, 0, wx.ALL, 0)
        
        # create some static text and add it to the box
        angle_text = wx.StaticText(self, -1, "Angle")
        angle_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        angle_text.SetSize(angle_text.GetBestSize())
        box.Add(angle_text, 0, wx.ALL, 0)
        # create a text control and add it to the box
        self.angle_input = wx.TextCtrl(self, value='45')
        box.Add(self.angle_input, 0, wx.ALL, 0)
        
        # Adds a check box for basemap
        self.basemap_cb = wx.CheckBox(self, -1, 'Basemap')
        self.basemap_cb.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.basemap_cb.SetSize(angle_text.GetBestSize())
        box.Add(self.basemap_cb, 0, wx.ALL, 0)

        # box.Add(MainPanel(self), 0, wx.ALL, 0)

        # Autosize the box and create a layout
        self.SetSizer(box)
        self.Layout()
      
        
        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpenDir, menuOpenDir)
        
       
        # Publisher().subscribe(self.showFrame, ("givelatlong"))
       
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
            dirpath = filesstuff[4]
            longslist = []  # more lists that need to be made
            latslistr = []  
            dmslist = []
            dpslist = []
            si = 0  
            Dmsitelist = []
            Imsitelist = []
            maxerror = float(self.perc_input.GetValue())
            maxangler = math.radians(float(self.angle_input.GetValue()))
            for si in range(0, len(sites)):                
                SiteWindow(frame, sites, si, cores, filepath, textfilename, maxerror, maxangler, dirpath).Show()
                # Publisher.subscribe(LatLongPage.onSendAndClose, 'getlatlong')

                NSSUM = 0
                EWSUM = 0
                UDSUM = 0
                CoreDmslist = []
                CoreImslist = []
                Rlist = []
                coresinsitelist = []  # this doesn't do anything,but I thought it would be useful to have
                N = 0    
                
                # This is all of the math for the individual sites.Everything should be self explanatory
                # siteanalysis.siteanalysis(sites, si, CoreDmslist, CoreImslist, Dmsitelist, Imsitelist, coresinsitelist, dmslist, latslistr, dpslist, longslist)
        dlg.Destroy()    
        
     
    

if __name__ == "__main__":
    app = wx.App(0)
    frame = MainWindow(None, "Pmag")
    app.MainLoop()
