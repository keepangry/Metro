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


def files_process_oneday(train_files):
    # station, day, timeslice, status
    counts = np.zeros((81, 2, 144))
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
            counts[stationID][status][timeslice] += 1
        fr.close()
    return counts


def output(predict, output_file):
    fw = open(output_file, 'w')
    fw.write('stationID,startTime,endTime,inNums,outNums')
    fw.write('\n')

    fr = open(os.path.join(BASE_PATH, 'dataset/Metro_testA/testA_submit_2019-01-29.csv'))
    fr.readline()
    for line in fr:
        stationID, startTime, endTime = line.strip().split(',')
        stationID = int(stationID)
        t = time.strptime(startTime, "%Y-%m-%d %H:%M:%S")
        timeslice = t.tm_hour * 6 + t.tm_min // 10
        write_line = "%s,%s,%s\n" % (line.strip(), predict[stationID][1][timeslice], predict[stationID][0][timeslice])
        fw.write(write_line)
    fw.close()
    fr.close()


def mae(predict_counts, valid_counts):
    return abs(np.mean(predict_counts-valid_counts))


if __name__ == "__main__":
    train_files = get_files('dataset/Metro_train')
    counts = files_process(train_files)

    # 整理出key的时间序列
    # station_in = counts[0][0].revel()

    predict = np.mean(counts, axis=2).astype('int')
    # 直接均值输出
    output(predict, "result/result_mean.csv")

    valid_counts_28 = files_process_oneday([os.path.join(BASE_PATH, 'dataset/Metro_testA/testA_record_2019-01-28.csv')])
    # valid_counts_25 = files_process_oneday([os.path.join(BASE_PATH, 'dataset/Metro_testA/testA_record_2019-01-28.csv')])

    # 全部平均：2.92
    print(mae(predict, valid_counts_28))

    # 对星期进行计算 1.7,1.14，1.21 => 1.28
    # 该星期平均： 1.60
    week_pred = np.mean(counts[:, :, [6, 13, 20], :], axis=2).astype('int')
    print(mae(week_pred, valid_counts_28))

    week_avg_pred = np.mean(counts[:, :, [0, 7, 14, 21], :], axis=2).astype('int')
    output(week_avg_pred, "result/week_avg_20190320.csv")

