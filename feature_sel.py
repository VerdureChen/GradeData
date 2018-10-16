#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:nieh
@file: main.py
@time: 2018/03/26
"""

from __future__ import division
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn import preprocessing
from utils.utils import *
from Features import Feature
import os
import numpy as np
import warnings
import sklearn.exceptions

warnings.filterwarnings('ignore', category=sklearn.exceptions.UndefinedMetricWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

if __name__ == "__main__":

    path = '/home1/nh/projects/Readability_v2/data/fine_grained/renjiaoban'  # 存放语料库的路径
    word_dict, char_dict, stroke_dict = construct_dict()

    feature = Feature(word_dict, char_dict, stroke_dict, path)

    if not os.path.exists('npy/fine_grained/rjb'):
        os.makedirs('npy/fine_grained/rjb')
    os.chdir('npy/fine_grained/rjb')

    if os.path.exists('X_ltp.npy') and os.path.exists('Y_ltp.npy'):
        print('分词模式：ltp segmentor')
        X = np.load('X_ltp.npy')
        Y = np.load('Y_ltp.npy')
        print('dataset loaded successfully!')
    else:
        feature.save_dataset()
        print('分词模式：ltp segmentor')
        X = np.load('X_ltp.npy')
        Y = np.load('Y_ltp.npy')
        print('dataset loaded successfully!')
    os.chdir('../../../')

    # 统计数据集中各类别的样本数目
    target_list = Y.tolist()
    u_target = set(target_list)
    for grade in u_target:
        print(grade, target_list.count(grade))

    min_max_scaler = preprocessing.MinMaxScaler()
    X_scaled = min_max_scaler.fit_transform(X)

    selector = SelectKBest(f_classif, k=10)
    selector.fit(X_scaled, Y)
    print selector.scores_