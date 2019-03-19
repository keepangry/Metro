#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-3-19 下午9:22
# @Author  : yangsen
# @Mail    : 0@keepangry.com
# @File    : method1_preprocess.py
# @Software: PyCharm
"""
使用prophet时间序列的方法进行预测

1、对历史数据按  站点、进出、时间片  进行分割，统计其数量
2、直接使用时间序列方法进行预测

"""
from common import *
import pandas as pd
import os
import numpy as np
import time

def files_process(train_files):
    # station, day, timeslice, status
    counts = np.zeros((81, 2, 25, 144))
    counter = 0

    for train_file in train_files:
        fr = open(train_file)
        fr.readline()
        for line in fr:
            counter += 1
            if counter % 10000 == 0:
                print(counter, train_file, np.sum(counts))
            time_, lineID, stationID, deviceID, status, userID, payType = line.strip().split(',')
            stationID = int(stationID)
            status = int(status)
            t = time.strptime(time_, "%Y-%m-%d %H:%M:%S")
            day = t.tm_mday-1
            timeslice = t.tm_hour * 6 + t.tm_min // 10
            counts[stationID][status][day][timeslice] += 1
        fr.close()
    return counts


if __name__ == "__main__":
    train_files = get_files('dataset/Metro_train')
    counts = files_process(train_files)

    # 整理出key的时间序列
    station_in = counts[0][0].revel()


