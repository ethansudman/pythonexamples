#!/usr/bin/env python

from Tkinter import *
import random
import kclus
try:
    import mclus
    mclus_present = True
except (Exception):
    mclus_present = False


class mainWindow:
    def __init__(self, master, title):
        self.window = master
        master.title(title)

        # Two frames: drawing canvas & controls
        ctlFrame = Frame(master)
        ctlFrame.pack()
        canvasFrame = Frame(master)
        canvasFrame.pack(fill=BOTH)
        
        Label(ctlFrame,text="Number of Clusters:").grid(row = 0,column = 0)
        self.clusterEntry = Entry(ctlFrame, width=2)
        self.nclusts = 3
        self.clusterEntry.insert(0, str(self.nclusts))
        self.clusterEntry.grid(row = 0,column = 1)
        self.spotsButton = Button(ctlFrame, text = "Generate Spots", command = self.genSpots).grid(row = 0, column = 3)
        self.goButton = Button(ctlFrame, text = "Go", command = self.go).grid(row = 0, column = 4)
        self.iterLabel = Label(ctlFrame, text="0", width=4, bg="white",
            justify=RIGHT)
        self.iterLabel.grid(row=0, column=5)
        #   Create drawing canvas
        self.xdim = 300
        self.ydim = 300
        self.canvas = Canvas(canvasFrame, bg="white", width=self.xdim+10, height=self.ydim+10)
        self.canvas.pack(fill=BOTH)
        
        self.pts = []
        self.window.mainloop()

    # Read number of clusters
    def readNClusters(self):
        s = self.clusterEntry.get()
        try:
            n = int(s)        
            if n < 2: n = 2
            if n > 5: n = 5
        except (ValueError):
            n = self.nclusts
        self.clusterEntry.delete(0, END)     #  Clean out display box.
        self.clusterEntry.insert(0, str(n))
        return n

    #  Called when Search button is hit.  Begin program.
    def genSpots(self):
        self.nclusts = self.readNClusters()
        print self.nclusts
        self.generated_centers = self.nclusts*[(0,0)]
        self.pts = []
        for clustno in range(self.nclusts):
            x = random.uniform(0.1, 0.9)
            y = random.uniform(0.1, 0.9)
            self.generated_centers[clustno] = (x,y)

            for i in range(40):
                pt = (random.gauss(x,0.10), random.gauss(y,0.10))
                if 0.0 < pt[0] < 1.0 and 0.0 < pt[1] < 1.0:
                    self.pts.append(pt)
        random.shuffle(self.pts)
        self.clear()
        self.plotpts()
        self.targets()

        print self.generated_centers, len(self.pts) 


    def clear(self):
        self.canvas.delete('all')
       
    def make_bbox(self, pt, r):
        cx = int(self.xdim*pt[0])+5
        cy = int(self.ydim*pt[1])+5
        return (cx-r, cy-r, cx+r, cy+r)

    def plotpts(self):
        for pt in self.pts:
            self.canvas.create_oval(*self.make_bbox(pt,2))

    def targets(self):
        for target in self.generated_centers:
            for r in 3, 6, 9:
                self.canvas.create_oval(*self.make_bbox(target,r))

    def showcenters(self, centers, color):
        for center in centers:
            bbox = self.make_bbox(center, 4)
            self.canvas.create_oval(bbox[0], bbox[1], bbox[2], bbox[3], 
                fill=color)

    def go(self):
        if len(self.pts) == 0:
            self.genSpots()
        print "go"
        if mclus_present:
            (centers, iters) = mclus.cluster(self.pts, self.nclusts)
            self.showcenters(centers, "green")
        (centers, iters) = kclus.cluster(self.pts, self.nclusts)
        self.showcenters(centers, "red")
        self.iterLabel.configure(text=str(iters))
            

if __name__ == "__main__":
    rootwindow = Tk()
    w = mainWindow(rootwindow, "CS332 Clustering")
