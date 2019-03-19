#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-3-19 下午9:25
# @Author  : yangsen
# @Mail    : 0@keepangry.com
# @File    : common.py
# @Software: PyCharm
import os
BASE_PATH = '/home/yangsen/workspace/Metro'
import time



def get_files(dir):
    dir_path = os.path.join(BASE_PATH, dir)
    return [os.path.join(dir_path, file_name) for file_name in os.listdir(dir_path)]


if __name__ == "__main__":
    train_files = get_files('dataset/Metro_train')
    t = time.strptime('2019-01-19 00:00:03', "%Y-%m-%d %H:%M:%S")