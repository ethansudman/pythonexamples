#!env python
        
#  CS 290 Triangle Movement Program
#
#  Use the mouse to create a triangle (or other shape) a point at a time.
#
#  User input specifies various values for translating, shearing, 
#  and rotating the polygon.
#
from Tkinter import *
from sys import exit
import tkMessageBox
import adata
import astar
import time

from math import radians, sin, cos, tan



class mainWindow:

    def __init__(self,master,title):

        self.points = []
        self.window = master
        master.title(title)
        ctlframe=Frame(master)
        ctlframe.pack(side=LEFT)

        #  Menubar on top
        master.config(menu=self.makeMenus(master))

        #  Parameter frame: parameters for running the
        #  genetic algorithm (mostly a bunch of Entry text boxes)
        #
        mframe = Frame(ctlframe, bd=5, relief=GROOVE)
        mframe.grid(row=3, column=0, columnspan=2, pady=10)
       
        Label(mframe, text="Start City").grid(row=3, column=0, sticky=S+E)
        self.ainput=Entry(mframe, bg="white", width=25)
        self.ainput.insert(0, "Yakima, WA")
        self.ainput.grid(row=3, column=1)

        Label(mframe,text="End City").grid(row=4, column=0, sticky=S+E)
        self.binput=Entry(mframe, bg="white", width=25)
        self.binput.insert(0, "Tampa, FL")
        self.binput.grid(row=4, column=1)

        Label(mframe,text="Debug Opts").grid(row=5, column=0, sticky=S+E)
        self.dinput=Entry(mframe, bg="white", width=4)
        self.dinput.insert(0, "")
        self.dinput.grid(row=5, column=1)

        #  Ctrl Frame:  Reset and Go
        Label(ctlframe, bg="white", \
            text="CS 332 A* Path Finding Visualizer").grid(\
                row=0, column=0, columnspan=2, pady=10)
        self.startButton=Button(ctlframe, text="Start", command=self.start)
        self.startButton.grid(row=1, column=0, pady=40, sticky=N+S)
        #self.pauseButton=Button(ctlframe, text="Pause", command=self.pause, \
        #            width=8)
        #self.pauseButton.grid(row=1, column=1, pady=40, sticky=N+S)

        #  Status Frame inside Ctl Frame
        #        
        self.statframe = Frame(ctlframe)
        self.statframe.grid(row=4, column=0, columnspan=2, pady=10)

        Label(self.statframe, text="Visited").grid(row=0, column=0)
        Label(self.statframe, text="Length").grid(row=1, column=0)
        #Label(self.statframe, text="Longest").grid(row=2, column=0)
        self.statv = Label(self.statframe, "", bg="white", width=9, 
            justify=RIGHT)
        self.statv.grid(row=0, column=1, sticky=W)
        self.statl = Label(self.statframe, "", bg="white", width=9, 
            justify=RIGHT)
        self.statl.grid(row=1, column=1, sticky=W)
        #self.statl = Label(self.statframe, "", bg="white", width=9,
        #   justify=RIGHT)
        #self.statl.grid(row=2, column=1, sticky=W)
        
        
        #  Drawing Canvas
        #
        self.canvasframe = Frame(master, bd=5, relief=GROOVE)
        self.canvasframe.pack(side=RIGHT)
        self.newcanvas()
        self.pathid = None

    def newcanvas(self):
        self.canvas = Canvas(self.canvasframe, bg="white", width=450, height=330)
        self.canvas.grid(row=0, column=0)
        self.xscale=400
        self.yscale=300

        # Mouse button action
        #self.canvas.bind("<Button-1>", self.mouseSelect)

        self.draw_all_cities()
        self.draw_all_roads()
        
    
    #  Menus (on the top menu bar)
    #
    def makeMenus(self,frame):
        returner=Menu(frame)
    
        #  Your usual 'file' menu a 'quit'  
        fileMenu=Menu(returner,tearoff=0)
        returner.add_cascade(label="File",menu=fileMenu)
        fileMenu.add_command(label="Quit",command=frame.quit)
    
        #  A 'help' menu contains only 'about'
        helpMenu=Menu(returner,tearoff=0)
        returner.add_cascade(label="Help",menu=helpMenu)
        helpMenu.add_command(label="About",command=self.about)

        return returner

    #  'Start' button handler: 
    #
    def start(self):
        
        self.startcity = getstr(self.ainput)
        self.goalcity = getstr(self.binput)
        if not self.startcity in adata.cities:
            self.ainput.config(text="***")
            return
        if not self.goalcity in adata.cities:
            self.binput.config(text="***")
            return

        for item in self.canvas.find_withtag("marked"):
            self.canvas.itemconfig(item, fill="#ccc")
            self.canvas.dtag(item, "marked")
        self.visited=0
        self.glen=0
        self.dbg     = getstr(self.dinput)
        self.astar = astar.AS(self.startcity, self.goalcity,
                              lambda x: self.updateroute(x))
        # self.ainput.delete(0,len(self.cinput.get()))
        # self.cinput.insert(0,str(self.ncities))
        # self.genno = 0
        # self.newcanvas()
        # self.drawpath(self.ga.population[0])
        # self.best_pathlen = 0
        # self.worst_pathlen = 0
        # self.recall = self.canvas.after(10, self.nextgen)
        route = self.astar.astar_run(self.dbg)
        self.statupdate("white")
        self.markroute(route, "red")

    def updateroute(self, n):
        print "Visiting", n.toString()
        self.visited = self.visited + 1
        self.glen = n.g
        for marked_item in self.canvas.find_withtag("marked"):
            self.canvas.itemconfig(marked_item, fill="green")
        self.markroute(n, "red")
        self.statupdate("yellow")
        #self.canvas.after(1)
        #self.canvas.event_generate("<Button-1>")
        #time.sleep(0.1)
        
    def markroute(self, n, color):
        path = n.path
        pairs = zip(path[:-1],path[1:])
        for pair in pairs:
            self.mark_road(pair[0], pair[1], color)
        

    def statupdate(self, color):
        self.statv.configure(text=str(self.visited), bg=color)
        self.statl.configure(text=str(self.glen), bg=color)
        #self.statl.configure(text=str(self.worst_pathlen), bg=color)

    """
    def nextgen(self):
        if self.genno < self.ngens:
            self.genno, self.best_path, self.best_pathlen, \
                self.worst_pathlen = self.ga.run_ga(5)
            self.drawpath(self.best_path)
            self.statupdate("yellow")
            self.recall = self.canvas.after(10, self.nextgen)
        else:
            self.statupdate("white")
    """
    
    #  Pause/Continue are not operational
    #
    def pause(self):
        self.canvas.after_cancel(self.recall)
        self.pauseButton.configure(text="Continue", command=self.contin)

    def contin(self):
        self.pauseButton.configure(text="Pause   ", command=self.pause)
        self.recall = self.canvas.after(10, self.nextgen)
 
    # Now draw a path
    """
    def drawpath(self, path):
        if self.pathid:
            self.canvas.delete(self.pathid)
        else:
            self.draw_some_cities(path)

        if len(path) > 1:
            loclist = [tspdata.scaledloc(c) for c in path]
            vertexlist = []
            for yr, xr in loclist:
                vertexlist.append(scalept(xr,self.xscale))
                vertexlist.append(scalept(yr,self.yscale))
            yr, xr = loclist[0]
            vertexlist.append(scalept(xr,self.xscale))
            vertexlist.append(scalept(yr,self.yscale))
            
            self.pathid=self.canvas.create_line(*vertexlist)
    """
    
    def draw_all_cities(self):
        xrmin = 1.0
        yrmin = 1.0
        xrmax = 0.0
        yrmax = 0.0
        for c in adata.cities:
            yr, xr = adata.scaledloc(c)
            xrmin = min(xrmin, xr)
            yrmin = min(yrmin, yr)
            xrmax = max(xrmax, xr)
            yrmax = max(yrmax, yr)
            x0, y0 = (scalept(xr, self.xscale), scalept(yr, self.yscale))
            self.canvas.create_oval(x0-2, y0-2, x0+2, y0+2,\
                                    fill="green", tags=self.maketag(c))

    def mark_city(self, city):
        tag = self.maketag(city)
        self.canvas.itemconfig(tag,fill="red")
        self.canvas.addtag_withtag("marked", tag)

    def mark_road(self, c1, c2, color):
        tag = self.makeroad(c1, c2)
        self.canvas.itemconfig(tag,fill=color)
        self.canvas.addtag_withtag("marked", tag)

        
    def draw_all_roads(self):
        for c1 in adata.cities:
            for c2 in adata.roadlist(c1):
                if c1 > c2: continue
                self.draw_one_road(c1, c2, '#ccc')
                                   
    def draw_one_road(self, c1, c2, color):
        road = self.makeroad(c1, c2)
        y1, x1 = adata.scaledloc(c1)
        y2, x2 = adata.scaledloc(c2)
        x1, y1 = (scalept(x1, self.xscale), scalept(y1, self.yscale))
        x2, y2 = (scalept(x2, self.xscale), scalept(y2, self.yscale))
        self.canvas.create_line(x1, y1, x2, y2, fill=color, tags=road)
 
        
    def makeroad(self, c1, c2):
        if c1 > c2:
            return self.makeroad(c2, c1)
        return self.maketag('$'.join([c1, c2]))

    def maketag(self, c):
        return c.replace(" ", "-")
    
    def about(self):
        tkMessageBox.showinfo("About", "A* Path Finder for CS332")

# Get string from text widget
def getstr(textwid):
    try:
        val = textwid.get()
    except:
        val = ""
    return val

# Convert string to integer
def cvt(textwid):
    try:
        val = int(textwid.get())
    except:
        val = 0
    return val

def scalept(x, scale):
    return int(round((1-x)*scale))+15

#  Main Program
#
if __name__=="__main__":

    w = Tk()
    adata.input()
    cs332_window = mainWindow(w, "CS 332 A* Path Finder")

    #  Wait for something to happen!
    cs332_window.window.mainloop()
