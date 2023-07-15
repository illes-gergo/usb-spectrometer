import numpy as np
import tkinter as tk
import seabreeze.spectrometers as sp
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import threading
import time

def InitPlotArea():
    global a, f, canvas
    f = Figure(figsize=(6,6),dpi=100)
    a = f.add_subplot(1,1,1)
    a.set_xlabel("Wavelength (nm)")
    a.set_ylabel("Intenisty (arb. u.)")

    canvas = FigureCanvasTkAgg(f,master=plotframe)
    canvas.draw()

    toolbar=NavigationToolbar2Tk(canvas, plotframe, pack_toolbar=False)

    toolbar.pack(side=tk.TOP,expand=True,fill=tk.X)
    canvas.get_tk_widget().pack(fill=tk.BOTH,expand=True)

def matplotCanvas(wavelengths,intensities):
    global a, f, canvas
    a.axes.clear()
    a.set_xlabel("Wavelength (nm)")
    a.set_ylabel("Intenisty (arb. u.)")
    if deadpxcorr.get()==1:
        intensities[1] = (intensities[0] + intensities[2])/2
        intensities[1300] = (intensities[1299] + intensities[1301])/2
    a.plot(wavelengths,intensities)
    canvas.draw()
    
def matplotCanvasBTN():
    if backcal.get()==0: intensities = processedData.copy()
    elif backcal.get()==1: intensities = np.subtract(processedData,backcaldata)
    if deadpxcorr.get()==1:
        intensities[1] = (intensities[0] + intensities[2])/2
        intensities[1300] = (intensities[1299] + intensities[1301])/2
    global a, f, canvas
    a.axes.clear()
    a.set_xlabel("Wavelength (nm)")
    a.set_ylabel("Intenisty (arb. u.)")
    a.plot(spec.wavelengths(),intensities)
    canvas.draw()
    
def acqdata():
    global processedData
    spec.open()
    spec.integration_time_micros(float(timeentry.get())*1e3)
    avgcount = int(avgentry.get())
    DATA=[[0]*len(spec.wavelengths())]*avgcount
    
    if avgcount == 1:
        processedData = spec.intensities()
    else:
        for i in range(avgcount):
            DATA[i] = spec.intensities()
        processedData = np.divide(np.sum(DATA,axis=0),avgcount)
    spec.close()

    if backcal.get() == 0: matplotCanvas(spec.wavelengths(),processedData)
    if backcal.get() == 1: matplotCanvas(spec.wavelengths(),np.subtract(processedData,backcaldata))

def acqbackcalib():
    spec.open()
    spec.integration_time_micros(float(timeentry.get())*1e3)
    avgcount = int(avgentry.get())
    DATA=[[0]*len(spec.wavelengths())]*avgcount
    
    if avgcount == 1:
        processedData = spec.intensities()
    else:
        for i in range(avgcount):
            DATA[i] = spec.intensities()
        processedData = np.divide(np.sum(DATA,axis=0),avgcount)
    spec.close()
    global backcaldata
    backcaldata = processedData


def fsave():
    f = open(fileentry.get(),"w")
    correctedData = processedData.copy()
    correctedData[1] = (correctedData[0] + correctedData[2])/2
    correctedData[1300] = (correctedData[1299] + correctedData[1301])/2
    correctedBackData = backcaldata.copy()
    correctedBackData[1] = (correctedBackData[0] + correctedBackData[2])/2
    correctedBackData[1300] = (correctedBackData[1299] + correctedBackData[1301])/2
    np.savetxt(f,np.transpose([spec.wavelengths(),processedData,correctedData,backcaldata,np.subtract(correctedData,correctedBackData)]))

def contacq():
    while contmode:
        acqdata()
        time.sleep(0.01)

def contstart():
    global contmode
    contmode = True
    timeentry.config(state="disabled")
    avgentry.config(state="disabled")
    measbutton.config(state= "disabled")
    plotbutton.config(state="disabled")
    filesavebutton.config(state="disabled")
    contstartbutton.config(state="disabled")
    bcksetbutton.config(state="disabled")
    threading.Thread(target=contacq).start()
    

def contstop():
    global contmode
    contmode=False
    timeentry.config(state="normal")
    avgentry.config(state="normal")
    measbutton.config(state= "normal")
    plotbutton.config(state="normal")
    filesavebutton.config(state="normal")
    contstartbutton.config(state="normal")
    bcksetbutton.config(state="normal")

spec = sp.Spectrometer.from_serial_number()
backcaldata = [0]*spec.wavelengths()
processedData = [0]*spec.wavelengths()
window = tk.Tk()
backcal = tk.IntVar(value=0)
deadpxcorr = tk.IntVar(value=0)
contmode = False

title = tk.Label(master=window, text="OceanOptics USB2000+ software by IG",font=16)
title.pack()
plotframe = tk.Frame(master=window, width=600,height=600)
plotframe.pack(fill=tk.BOTH,side=tk.LEFT,expand=True)
setframe = tk.Frame(master=window, width=300,height=600)
setframe.pack(fill=tk.BOTH,side=tk.LEFT,expand=False)
plotbutton = tk.Button(master=setframe,text="Plot",font=16,command=matplotCanvasBTN)

plotbutton.grid(row=8,column=1,columnspan=1,padx=5,pady=5)
measbutton = tk.Button(master=setframe,text="Measure and plot",font=16,command=acqdata)

measbutton.grid(row=8,column=2,columnspan=1,padx=5,pady=5)

timelabel = tk.Label(master=setframe,text="Integration time (ms)",font=16)
timeentry = tk.Entry(master=setframe,font=16, justify=tk.CENTER)
timeentry.insert(0,"100")
timelabel.grid(row=1,column=1,padx=5, pady=5)
timeentry.grid(row=2,column=1,padx=5, pady=5)


avglabel = tk.Label(master=setframe,text="Averaging count",font=16)
avgentry = tk.Entry(master=setframe,font=16, justify=tk.CENTER)
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

deadlabel = tk.Label(master=setframe,text="Hard-coded dead pixel correction")
deadoff = tk.Radiobutton(master=setframe, text = "Off", variable=deadpxcorr, value=0)
deadon = tk.Radiobutton(master=setframe, text = "On", variable=deadpxcorr, value=1)
deadlabel.grid(row=6,column=1,columnspan=2,padx=5,pady=6)
deadoff.grid(row=7,column=1,padx=5,pady=6)
deadon.grid(row=7,column=2,padx=5,pady=6)

filelabel = tk.Label(master=setframe,text="Saving data to file",font=16)
filelabel.grid(row=9,column=1, columnspan=2, padx=5, pady=5)
fileentry = tk.Entry(master=setframe,font=14,width=36, justify=tk.CENTER)
fileentry.insert(index=0,string="measurement.txt")
fileentry.grid(row=10,column=1, columnspan=2, padx=5, pady=5)
filesavebutton = tk.Button(master=setframe,text="Save",command=fsave)
filesavebutton.grid(row=11,column=1,columnspan=2,padx=5,pady=5)

contlabel = tk.Label(master=setframe,text="Continous Mode",font=16)
contlabel.grid(row=12,column=1, columnspan=2, padx=5, pady=5)

contstartbutton = tk.Button(master=setframe,text="Start", font=14 ,command=contstart)
contstartbutton.grid(row=13,column=1,columnspan=1,padx=5,pady=5)

contstopbutton = tk.Button(master=setframe,text="Stop", font=14 ,command=contstop)
contstopbutton.grid(row=13,column=2,columnspan=1,padx=5,pady=5)


InitPlotArea()


window.mainloop()