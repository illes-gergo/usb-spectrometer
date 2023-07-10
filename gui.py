import numpy as np
import tkinter as tk
import seabreeze.spectrometers as sp
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

def matplotCanvas(wavelengths,intensities):
    global plotted, a, f, canvas
    if plotted==False:
        f = Figure(figsize=(6,6),dpi=100)
        a = f.add_subplot(111)
    if plotted: a.axes.clear()
    a.plot(wavelengths,intensities)
    if plotted == False: canvas = FigureCanvasTkAgg(f,master=plotframe)
    canvas.draw()
    if plotted == False: canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True); toolbar=NavigationToolbar2Tk(canvas,plotframe)
    
    if plotted== False: canvas._tkcanvas.pack(fill=tk.BOTH, expand=True,side=tk.TOP); plotted = True
    
def matplotCanvasBTN():
    if backcal.get()==0: intensities = processedData
    else: intensities = np.subtract(processedData,backcaldata)
    global plotted, a, f, canvas
    if plotted==False:
        f = Figure(figsize=(6,6),dpi=100)
        a = f.add_subplot(111)
    if plotted: a.axes.clear()
    a.plot(spec.wavelengths(),intensities)
    if plotted == False: canvas = FigureCanvasTkAgg(f,master=plotframe)
    canvas.draw()
    if plotted == False: canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True); toolbar=NavigationToolbar2Tk(canvas,plotframe)
    
    if plotted== False: canvas._tkcanvas.pack(fill=tk.BOTH, expand=True,side=tk.TOP); plotted = True
    
def acqdata():
    global processedData
    spec.open()
    spec.integration_time_micros(float(timeentry.get())*1e6)
    avgcount = int(avgentry.get())
    DATA=[[0]*len(spec.wavelengths())]*avgcount
    
    if avgcount == 1:
        processedData = spec.intensities()
    else:
        for i in range(avgcount):
            DATA[i] = spec.intensities()
        processedData = np.sum(DATA,axis=0)/avgcount
    spec.close()

    if backcal.get() == 0: matplotCanvas(spec.wavelengths(),processedData)
    if backcal.get() == 1: matplotCanvas(spec.wavelengths(),np.subtract(processedData,backcaldata))

def acqbackcalib():
    spec.open()
    spec.integration_time_micros(float(timeentry.get())*1e6)
    avgcount = int(avgentry.get())
    DATA=[[0]*len(spec.wavelengths())]*avgcount
    
    if avgcount == 1:
        processedData = spec.intensities()
    else:
        for i in range(avgcount):
            DATA[i] = spec.intensities()
        processedData = np.sum(DATA,axis=0)/avgcount
    spec.close()
    global backcaldata
    backcaldata = processedData

plotted = False
spec = sp.Spectrometer.from_serial_number()
backcaldata = [0]*spec.wavelengths()
processedData = [0]*spec.wavelengths()
window = tk.Tk()
backcal = tk.IntVar()
title = tk.Label(master=window, text="OceanOptics USB2000+ software by IG",font=16)
title.pack()
plotframe = tk.Frame(master=window, width=600,height=600)
plotframe.pack(fill=tk.BOTH,side=tk.LEFT,expand=True)
setframe = tk.Frame(master=window, width=300,height=600)
setframe.pack(fill=tk.BOTH,side=tk.LEFT,expand=True)
plotbutton = tk.Button(master=setframe,text="Plot",font=16,command=matplotCanvasBTN)

plotbutton.grid(row=6,column=1,columnspan=1,padx=5,pady=6)
measbutton = tk.Button(master=setframe,text="Measure and plot",font=16,command=acqdata)

measbutton.grid(row=6,column=2,columnspan=1,padx=5,pady=6)

timelabel = tk.Label(master=setframe,text="Integration time (s)",font=16)
timeentry = tk.Entry(master=setframe,font=16)
timeentry.insert(0,"1")
timelabel.grid(row=1,column=1,padx=5, pady=5)
timeentry.grid(row=2,column=1,padx=5, pady=5)


avglabel = tk.Label(master=setframe,text="Averaging count",font=16)
avgentry = tk.Entry(master=setframe,font=16)
avgentry.insert(0,"1")

avglabel.grid(row=1,column=2,padx=5, pady=5)
avgentry.grid(row=2,column=2,padx=5, pady=5)

bcklabel = tk.Label(master=setframe,text="Background correction")
bckoff = tk.Radiobutton(master=setframe,text="Off", variable=backcal,value=0)
bckon = tk.Radiobutton(master=setframe,text="On", variable=backcal, value=1)
bcklabel.grid(row=3,column=1,columnspan=2,padx=5,pady=6)
bckoff.select()
bckon.grid(row=4,column=2,padx=5,pady=6)
bckoff.grid(row=4,column=1,padx=5,pady=6)

bcksetbutton = tk.Button(master=setframe,text="Set background reference data",command=acqbackcalib)
bcksetbutton.grid(row=5,column=1,columnspan=2,padx=5,pady=6)
window.mainloop()