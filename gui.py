import tkinter as tk
import seabreeze.spectrometers as sp
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

spec = sp.Spectrometer.from_serial_number()

def matplotCanvas():
    spec.open()
    f = Figure(figsize=(6,6),dpi=100)
    a = f.add_subplot(111)
    a.plot(spec.wavelengths(),spec.intensities())
    canvas = FigureCanvasTkAgg(f,master=plotframe)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    toolbar=NavigationToolbar2Tk(canvas,plotframe)
    canvas._tkcanvas.pack(fill=tk.BOTH, expand=True,side=tk.TOP)
    spec.close()

spec.integration_time_micros(1e6)
window = tk.Tk()
title = tk.Label(master=window, text="OceanOptics USB2000+ software by IG",font=16)
title.pack()
plotframe = tk.Frame(master=window, width=600,height=600,bg="blue")
plotframe.pack(fill=tk.BOTH,side=tk.LEFT,expand=True)
setframe = tk.Frame(master=window, width=300,height=600,bg="red")
setframe.pack(fill=tk.BOTH,side=tk.LEFT,expand=True)
matplotCanvas()

window.mainloop()