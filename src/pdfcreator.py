'''
Created on Apr 27, 2013

Based off of the first part of coreanalysis. creates our standard pdf
'''

from __future__ import division
import linecache
import math
import pylab
import stereoplot
import matplotlib.image as mpimg
import addimagepage
from PIL import Image, ImageDraw, ImageFont

def pdfcreator(si, sites, filepath, i, textfilename, maxerror, cores, maxangler, dirpath):
    if sites[si] in filepath[i]:
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
                magslist = []
                
                # creates the table for the pdf
                # tableline= [demagsteps[foo]+" "+magnitude[foo]+" "+declination[foo]+" "+inclination[foo] for foo in range(0,len(demagsteps))]
                tablelinelist = [[demagsteps[foo], magnitude[foo], declination[foo], inclination[foo] ] for foo in range(0, len(demagsteps))]
                # tablelinelist.insert(0, ['TR', 'Intensity', 'Dec', 'Inc'])
                tablestring = 'TR, Intensity, Dec, Inc \n'
                for foo in range(0, len(tablelinelist)):
                    tablestring = tablestring + ','.join(tablelinelist[foo]) + '\n'
                
                img = Image.new('RGB', (600, 600), (255, 255, 255))
                draw = ImageDraw.Draw(img)
                offset = 20
                # font = ImageFont.truetype("arial.ttf", 15)
                usefont = ImageFont.truetype('arial.ttf', 50)
                for foo in range(0, len(tablestring.splitlines())):
                    text = tablestring.splitlines()[foo]
                    draw.text((0, offset), text, fill=(0, 0, 0), font=usefont)  # string goes here
                    offset += 50
                del draw
                img.save('image.png')
                
                
                img = mpimg.imread('image.png')
                pylab.subplot(2, 2, 4, frameon=False, xticks=[], yticks=[])
                pylab.plt.imshow(img)
                pylab.savefig('test.png')
                
                
                for n in range (0, len(inclination)):  # loop does the math to take inclinations and declinations and turn them into core ns, ew, ud
                    incrad = math.radians(float(inclination[n]))                
                    decrad = math.radians(float(declination[n]))                 
                    mag = float(magnitude[n]) 
                    magslist.append(mag)
                    ns.append(mag * math.cos(decrad) * math.cos(incrad))
                    ew.append(mag * math.cos(incrad) * math.sin(decrad))
                    ud.append(mag * math.sin(incrad))
                declination = [float(foo) for foo in declination]
                inclination = [float(foo) for foo in inclination]
               
                
                pylab.subplot(2, 2, 2)
                stereoplot.stereoplot(declination, inclination, textfilename[i])
                
                pylab.subplot(2, 2, 3)
                normmagslist = [foo * 1 / magslist[0] for foo in magslist]
                pylab.plot(demagsteps, magslist, "-o")
                pylab.plot(demagsteps, normmagslist, "-o")
                pylab.xlabel('Demag Step (mT)')
                pylab.ylabel('Magnitude (A/m)')
                pylab.title('Magnitude')
                pylab.axhline(linewidth=1, color='k')
                pylab.axvline(linewidth=1, color='k')
                
                
                
                pylab.subplot(2, 2, 1)
                # makes plots
                negew = []  # zeiderfeld plots use negative axis 
                negud = []
                for n in range(0, len(ew)):
                    negew.append(-1 * ew[n])
                    negud.append(-1 * ud[n])   
                pylab.plot(ns, negew, "-o", label='NS vs -EW') + pylab.plot(ns, negud, "-o", label='NS vs -UD')  # actually does the plotting
                pylab.xlabel('-EW and -UD (A/m)')
                pylab.ylabel('NS (A/m)')
                pylab.title('Zijderveld Plot')
                pylab.axhline(linewidth=1, color='k')
                pylab.axvline(linewidth=1, color='k')
                pylab.axis('equal')
                pylab.legend(loc=1)
                pylab.tight_layout()
                pylab.savefig(cores[i] + "_pack.png")
                addimagepage.addimagepage(cores[i], "_pack.png")
                pylab.clf()
                # filelist = [ f for f in os.listdir(".") if f.endswith(".png") ]
                # for f in filelist:
                #    os.remove(f)
