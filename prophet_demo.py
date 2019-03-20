#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-3-19 下午9:59
# @Author  : yangsen
# @Mail    : 0@keepangry.com
# @File    : prophet_demo.py
# @Software: PyCharm
import pandas as pd
from fbprophet import Prophet
import numpy as np
import time

value = np.array([np.array(['2019-01-19 00:10:00', 3]),
                 np.array(['2019-01-19 00:20:00', 4]),
                 np.array(['2019-01-19 00:30:00', 3])])

df = pd.DataFrame(value, columns=["ds", "y"])



def index_to_datetime(day_index, timeslice_index):
    base_stamp = 1546272000
    stamp = base_stamp + day_index*24*3600 + timeslice_index*600
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stamp))





station1_in = counts[0][1]
nums = []
for day in range(station1_in.shape[0]):
    for timeslice in range(station1_in.shape[1]):
        datetime = index_to_datetime(day, timeslice)
        print(datetime)
        nums.append([datetime, station1_in[day][timeslice]])
df = pd.DataFrame(nums, columns=["ds", "y"])
df['floor'] = 0


m = Prophet(growth='logistic')
m.fit(df)
future = m.make_future_dataframe(periods=6*24*4, freq='10min', include_history=False)
df['floor'] = 0

forecast = m.predict(future)
forecast[['ds', 'yhat']]


fig1 = m.plot(forecast)
fig1.show()
