import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


my_data = pd.read_csv('data.csv', sep=',')

# From http://www.bom.gov.au/climate/data/
bom_data = pd.read_csv('IDCJAC0010_040211_2022_Data.csv', sep=',')


print(my_data)

plt.figure('Tempurature')

pins = {4:"Roof", 17:"Interior"}

my_data.date = pd.to_datetime(my_data['date'], format='%Y-%m-%d-%H-%M-%S')
df = pd.DataFrame({'year': bom_data.Year,
                   'month': bom_data.Month,
                   'day': bom_data.Day})
bom_data.date = pd.to_datetime(df)



for pin, label in pins.items():
  ind = my_data["pin"] == pin
  plt.plot(my_data.date[ind], my_data.temperature[ind],  label=label)

plt.plot(bom_data.date, bom_data["Maximum temperature (Degree C)"], label='Archerfield Daily Max (BOM)')

# Set the ticks
locs, labels = plt.yticks()
plt.yticks(np.arange(locs[0], locs[-1], 1))

plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))

plt.gcf().autofmt_xdate()

plt.xlabel("Date")
plt.ylabel("Temperature (C)")

plt.legend()
plt.grid()


# import scipy
# import scipy.fft
# from scipy.fft import fft, fftfreq


# # Sample spacing (half hourly)
# T = 1/2.0;
# ind = my_data["pin"] == 17
# y = my_data.temperature[ind].to_numpy()
# N = len(y)
# yf = fft(y)
# xf = fftfreq(N, T)[:N//2]

# plt.figure()
# plt.plot(1/xf, 2.0/N * np.abs(yf[0:N//2]))
# plt.grid()

plt.show()