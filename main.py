from seabreeze.spectrometers import Spectrometer
import matplotlib.pyplot as plt
spec = Spectrometer.from_first_available()
spec.integration_time_micros(2e6)
wl, darksa = spec.spectrum()
input("Fekete kalibrálás megtörtént!")
plt.plot(wl, spec.intensities()-darksa)
plt.show()
spec.close()