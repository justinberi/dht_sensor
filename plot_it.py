import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


my_data = pd.read_csv('data.csv', sep=',')

# From http://www.bom.gov.au/climate/data/
bom_data = pd.read_csv('IDCJAC0010_040211_2022_Data.csv', sep=',')


print(my_data)


pins = {4:"Roof", 17:"Interior"}
ind4 = my_data["pin"] == 4
ind17 = my_data["pin"] == 17

my_data.date = pd.to_datetime(my_data['date'], format='%Y-%m-%d-%H-%M-%S', utc=True)
my_data.date = my_data.date.dt.tz_convert("Australia/Brisbane")

# Find the max between 9am and 9am
# Day after
day0 = pd.to_datetime("2021-12-31-09-00-00", format='%Y-%m-%d-%H-%M-%S', utc=False)
day0 = day0.tz_localize("Australia/Brisbane")

day1 = pd.to_datetime("2022-01-01-09-00-00", format='%Y-%m-%d-%H-%M-%S', utc=False)
day1 = day1.tz_localize("Australia/Brisbane")

hrs24 = pd.DateOffset(days=1)

data_max = {"date":[], "temperature":[]}
while day0 < my_data.date.iloc[-1]:
  pin = 17
  temp = my_data[ind17]

  # All temperatures in the date range
  ind = np.logical_and(day0 <= temp.date, temp.date < day1)
  temp = temp[ind]

  # The time of the max
  ind = temp.temperature.idxmax()
  data_max["temperature"].append(temp.temperature[ind])
  data_max["date"].append(temp.date[ind])

  day0 = day0 + hrs24
  day1 = day1 + hrs24

data_max["date_daily_max"] = [pd.to_datetime("{}-{}-{}-{}".format(i.year, i.month, i.day, 9), format='%Y-%m-%d-%H', utc=False) for i in data_max["date"]]  # 9am of the day after
data_max["date_daily_max"] = [i.tz_localize("Australia/Brisbane") for i in data_max["date_daily_max"]]


# Create the bom date
df = pd.DataFrame({'year': bom_data.Year,
                   'month': bom_data.Month,
                   'day': bom_data.Day})
hrs9 = pd.DateOffset(hours=9)
bom_data.date = pd.to_datetime(df) + hrs9
bom_data.date = bom_data.date.dt.tz_localize("Australia/Brisbane")


plt.figure('Tempurature')

for pin, label in pins.items():
  ind = my_data["pin"] == pin
  plt.plot(my_data.date[ind], my_data.temperature[ind],  label=label)

plt.plot(bom_data.date, bom_data["Maximum temperature (Degree C)"], label='Archerfield Daily Max (BOM)')

plt.plot(data_max["date"], data_max["temperature"], '.', label='Max Interior')
plt.plot(data_max["date_daily_max"], data_max["temperature"], '.', label='Max Interior 9am')


# Set the ticks
locs, labels = plt.yticks()
plt.yticks(np.arange(locs[0], locs[-1], 1))

plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))

plt.gcf().autofmt_xdate()

plt.xlabel("Date")
plt.ylabel("Temperature (C)")

plt.legend()
plt.grid()

plt.figure('Tempurature Difference')

plt.plot(my_data.date[ind4], my_data.temperature[ind4].to_numpy()-my_data.temperature[ind17].to_numpy(),  label="Roof-Interior")

# Create a interpolant for the bom data (nearest cause it is sparse)
import scipy
import scipy.interpolate

#https://stackoverflow.com/questions/14313510/how-to-calculate-rolling-moving-average-using-python-numpy-scipy/54628145#54628145
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

bom_interpolant = scipy.interpolate.interp1d(bom_data.date.astype(int).to_numpy(), bom_data["Maximum temperature (Degree C)"].to_numpy(), kind='nearest', bounds_error=False)
bom_aligned = bom_interpolant(my_data.date[ind4].astype(int).to_numpy())
diff = my_data.temperature[ind17].to_numpy()-bom_aligned
plt.plot(my_data.date[ind4], diff,  label="Interior-BomMax")

bom_aligned = bom_interpolant(my_data.date[ind4].astype(int).to_numpy())
diff = my_data.temperature[ind4].to_numpy()-bom_aligned
plt.plot(my_data.date[ind4], diff,  label="Roof-BomMax")

r = 4*24
mavg = moving_average(diff, r)
plt.plot(my_data.date[ind4][r-1:], mavg,  label="moving average Interior-BomMax")

# plt.plot(bom_data.date, bom_data["Maximum temperature (Degree C)"], label='Archerfield Daily Max (BOM)')

# compare wit bom
dd = []
bom_date = []
for i in range(len(bom_data.date)):
  try:
    ind = data_max["date_daily_max"].index(bom_data.date.iloc[i])
  except:
    continue
  dd.append(data_max["temperature"][ind] - bom_data["Maximum temperature (Degree C)"].iloc[i])
  bom_date.append(bom_data.date.iloc[i])

plt.plot(bom_date, dd, label="InteriorMax-BomMax")


# Need the max in a given day
# Convert to local time?

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
