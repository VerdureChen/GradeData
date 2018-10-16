#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:nieh
@file: main.py
@time: 2018/03/26
"""

from __future__ import division
from sklearn import preprocessing
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from utils.utils import *
from Features import Feature
import os
import numpy as np
import math
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

    avg_acc = 0.0
    avg_std = 0.0
    for i in range(10):
        # 保留所有特征，计算评价指标
        print "##################################################################################################"
        print "###################################保留所有特征，指标如下###########################################"
        # 对数据集进行预处理
        min_max_scaler = preprocessing.MinMaxScaler()
        X_scaled = min_max_scaler.fit_transform(X)
        n_samples = X_scaled.shape[0]  # 样本总数
        print "样本总数为：", n_samples

        num_splits = 10
        estimator = svm.NuSVC()
        X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.4, shuffle=True,
                                                            stratify=Y)
        param_grid = {"nu": [0.25, 0.3, 0.35, 0.4], "kernel": ['rbf', 'poly'],
                      "degree": [1, 2, 3, 4, 5, 6],
                      "gamma": [0.125, 0.25, 0.4, 0.5, 0.6, 0.8, 1, 2, 3, 4, 5]}
        grid = GridSearchCV(estimator=estimator, param_grid=param_grid, scoring='accuracy', cv=num_splits, n_jobs=4)
        grid.fit(X_train, Y_train)
        print "Best parameters set found on development set:",
        print grid.best_params_
        print "Best grid scores on development set:",
        print grid.best_score_
        print
        print "Best estimator:"
        print grid.best_estimator_
        print
        for params, mean_score, scores in grid.grid_scores_:
            if params == grid.best_params_:
                print("%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() / 2, params))

        Y_true, Y_pred = Y_test, grid.predict(X_test)
        Y_true_list = []
        list1 = list(Y_true)
        for i in list1:
            if i == 'lev1':
                Y_true_list.append(1)
            elif i == 'lev2':
                Y_true_list.append(2)
            elif i == 'lev3':
                Y_true_list.append(3)
            elif i == 'lev4':
                Y_true_list.append(4)
            elif i == 'lev5':
                Y_true_list.append(5)
        Y_pred_list = []
        list2 = list(Y_pred)
        for i in list2:
            if i == 'lev1':
                Y_pred_list.append(1)
            elif i == 'lev2':
                Y_pred_list.append(2)
            elif i == 'lev3':
                Y_pred_list.append(3)
            elif i == 'lev4':
                Y_pred_list.append(4)
            elif i == 'lev5':
                Y_pred_list.append(5)
        err_std = 0.0
        sum_square = 0.0
        for i in range(len(Y_true_list)):
            sum_square += (Y_true_list[i] - Y_pred_list[i]) ** 2
        err_std = math.sqrt(sum_square / len(Y_true_list))
        acc = grid.score(X_test, Y_test)

        avg_std += err_std
        avg_acc += acc

        class_names = ['lev1', 'lev2', 'lev3', 'lev4', 'lev5']
        print
        print "Detailed classification report:"
        print "The model is trained on the full training set."
        print "The scores are computed on the full test set."
        print classification_report(Y_true, Y_pred, target_names=class_names)
        print "Accuracy:  %.3f" % acc
        print "Error Standard deviation:  %.3f" % err_std
        print

    print "Avg_acc: ", avg_acc / 10, "Avg_std: ", avg_std / 10

    # 进行烧灼测试，依次去掉某一个或者某一类特征，汇报相应的评价指标
    for i in range(18):
        print "##############################################################################################"
        print "###################################去掉第%d个特征，指标如下######################################" % (i + 1)
        X_deleted = np.delete(X, i, axis=1)  # 依次去掉数据矩阵X的某一列，删除相应的特征

        # 对数据集进行预处理
        min_max_scaler = preprocessing.MinMaxScaler()
        X_scaled = min_max_scaler.fit_transform(X_deleted)
        n_samples = X_scaled.shape[0]  # 样本总数
        print "样本总数为：", n_samples

        n_splits = 10
        estimator = svm.NuSVC()
        X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.4, random_state=3, shuffle=True, stratify=Y)
        param_grid = {"nu": [0.25, 0.3, 0.35, 0.4], "kernel": ['rbf', 'poly'],
                      "degree": [1, 2, 3, 4, 5, 6],
                      "gamma": [0.125, 0.25, 0.4, 0.5, 0.6, 0.8, 1, 2, 4]}
        grid = GridSearchCV(estimator=estimator, param_grid=param_grid, scoring='accuracy', cv=num_splits, n_jobs=4)
        grid.fit(X_train, Y_train)
        print "Best parameters set found on development set:",
        print grid.best_params_
        print "Best grid scores on development set:",
        print grid.best_score_
        print
        print "Best estimator:"
        print grid.best_estimator_
        print
        for params, mean_score, scores in grid.grid_scores_:
            if params == grid.best_params_:
                print("%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() / 2, params))

        Y_true, Y_pred = Y_test, grid.predict(X_test)
        Y_true_list = []
        list1 = list(Y_true)
        for i in list1:
            if i == 'lev1':
                Y_true_list.append(1)
            elif i == 'lev2':
                Y_true_list.append(2)
            elif i == 'lev3':
                Y_true_list.append(3)
            elif i == 'lev4':
                Y_true_list.append(4)
            elif i == 'lev5':
                Y_true_list.append(5)
        Y_pred_list = []
        list2 = list(Y_pred)
        for i in list2:
            if i == 'lev1':
                Y_pred_list.append(1)
            elif i == 'lev2':
                Y_pred_list.append(2)
            elif i == 'lev3':
                Y_pred_list.append(3)
            elif i == 'lev4':
                Y_pred_list.append(4)
            elif i == 'lev5':
                Y_pred_list.append(5)
        err_std = 0.0
        sum_square = 0.0
        for i in range(len(Y_true_list)):
            sum_square += (Y_true_list[i] - Y_pred_list[i]) ** 2
        err_std = math.sqrt(sum_square / len(Y_true_list))

        class_names = ['lev1', 'lev2', 'lev3', 'lev4', 'lev5']
        print
        print "Detailed classification report:"
        print "The model is trained on the full training set."
        print "The scores are computed on the full test set."
        print classification_report(Y_true, Y_pred, target_names=class_names)
        print "Accuracy:  %.3f" % grid.score(X_test, Y_test)
        print "Error Standard deviation:  %.3f" % err_std


    # # 保留所有特征，计算评价指标
    # print "##################################################################################################"
    # print "###################################保留所有特征，指标如下###########################################"
    # # 对数据集进行预处理
    # min_max_scaler = preprocessing.MinMaxScaler()
    # X_scaled = min_max_scaler.fit_transform(X)
    # n_samples = X_scaled.shape[0]  # 样本总数
    # print "样本总数为：", n_samples
    #
    # n_splits = 10
    # estimator = svm.NuSVC()
    # X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.4, random_state=2, stratify=Y)
    # param_grid = {"nu": [0.01, 0.03, 0.05, 0.07, 0.09, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4],
    #               "kernel": ['rbf', 'poly'], "degree": [1, 2, 3, 4, 5, 6],
    #               "gamma": [0.125, 0.25, 0.4, 0.5, 0.6, 0.8, 1, 2, 4]}
    # grid = GridSearchCV(estimator=estimator, param_grid=param_grid, cv=n_splits, n_jobs=4)
    # grid.fit(X_train, Y_train)
    # print "Best parameters set found on development set:",
    # print grid.best_params_
    # print "Best grid scores on development set:"
    # print grid.best_score_
    # print
    # print "Best estimator:"
    # print grid.best_estimator_
    # print
    # for params, mean_score, scores in grid.grid_scores_:
    #     if params == grid.best_params_:
    #         print("%0.3f (+/-%0.03f) for %r"
    #               % (mean_score, scores.std() / 2, params))
    #
    # Y_true, Y_pred = Y_test, grid.predict(X_test)
    # Y_true_list = []
    # list1 = list(Y_true)
    # for i in list1:
    #     if i == 'one':
    #         Y_true_list.append(1)
    #     elif i == 'two':
    #         Y_true_list.append(2)
    #     elif i == 'three':
    #         Y_true_list.append(3)
    #     elif i == 'four':
    #         Y_true_list.append(4)
    #     elif i == 'five':
    #         Y_true_list.append(5)
    #     elif i == 'six':
    #         Y_true_list.append(6)
    #     elif i == 'seven':
    #         Y_true_list.append(7)
    #     elif i == 'eight':
    #         Y_true_list.append(8)
    #     elif i == 'nine':
    #         Y_true_list.append(9)
    # Y_pred_list = []
    # list2 = list(Y_pred)
    # for i in list2:
    #     if i == 'one':
    #         Y_pred_list.append(1)
    #     elif i == 'two':
    #         Y_pred_list.append(2)
    #     elif i == 'three':
    #         Y_pred_list.append(3)
    #     elif i == 'four':
    #         Y_pred_list.append(4)
    #     elif i == 'five':
    #         Y_pred_list.append(5)
    #     elif i == 'six':
    #         Y_pred_list.append(6)
    #     elif i == 'seven':
    #         Y_pred_list.append(7)
    #     elif i == 'eight':
    #         Y_pred_list.append(8)
    #     elif i == 'nine':
    #         Y_pred_list.append(9)
    # err_std = 0.0
    # sum_square = 0.0
    # for i in range(len(Y_true_list)):
    #     sum_square += (Y_true_list[i] - Y_pred_list[i]) ** 2
    # err_std = math.sqrt(sum_square / len(Y_true_list))
    #
    # class_names = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    # print
    # print "Detailed classification report:"
    # print "The model is trained on the full training set."
    # print "The scores are computed on the full test set."
    # print classification_report(Y_true, Y_pred, target_names=class_names)
    # print "Accuracy:  %.3f" % grid.score(X_test, Y_test)
    # print "Error Standard deviation:  %.3f" % err_std
