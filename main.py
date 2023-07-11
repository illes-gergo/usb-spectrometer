from seabreeze.spectrometers import Spectrometer
import matplotlib.pyplot as plt
spec = Spectrometer.from_serial_number()
spec.integration_time_micros(2e6)
plt.plot(spec.intensities())
plt.show()
spec.close() # 2-ik és 1300-ik hibás