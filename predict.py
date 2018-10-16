#!usr/bin/env python  
# -*- coding:utf-8 -*-
""" 
@author:nieh 
@file: predict.py 
@time: 2018/03/29 
"""

from __future__ import division
from sklearn import preprocessing
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.utils import shuffle
from utils.utils import *
from Features import Feature
import pandas as pd
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
import os
import numpy as np
import math
import warnings
import sklearn.exceptions

warnings.filterwarnings('ignore', category=sklearn.exceptions.UndefinedMetricWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

if __name__ == "__main__":
    train_path = "/home1/nh/projects/Readability_v2/data/fine_grained/renjiaoban"
    test_path = "/home1/nh/projects/Readability_v2/data/fine_grained/sujiaoban"
    word_dict, char_dict, stroke_dict = construct_dict()
    print

    # 构造训练数据集
    if not os.path.exists('npy/fine_grained/rjb'):
        os.makedirs('npy/fine_grained/rjb')
    os.chdir('npy/fine_grained/rjb')
    if os.path.exists('X_ltp.npy') and os.path.exists('Y_ltp.npy'):
        print('分词模式：ltp segmentor')
        X_train = np.load('X_ltp.npy')
        Y_train = np.load('Y_ltp.npy')
        print('train dataset loaded successfully!')
    else:
        train_feature = Feature(word_dict, char_dict, stroke_dict, train_path)
        train_feature.save_dataset()
        print('分词模式：ltp segmentor')
        X_train = np.load('X_ltp.npy')
        Y_train = np.load('Y_ltp.npy')
        print('train dataset loaded successfully!')
    os.chdir('../../../')

    # 构造测试数据集
    if not os.path.exists('npy/fine_grained/sjb'):
        os.makedirs('npy/fine_grained/sjb')
    os.chdir('npy/fine_grained/sjb')

    if os.path.exists('X_ltp.npy') and os.path.exists('Y_ltp.npy'):
        print('分词模式：ltp segmentor')
        X_test = np.load('X_ltp.npy')
        Y_test = np.load('Y_ltp.npy')
        print('test dataset loaded successfully!')
    else:
        test_feature = Feature(word_dict, char_dict, stroke_dict, test_path)
        test_feature.save_dataset()
        print('分词模式：ltp segmentor')
        X_test = np.load('X_ltp.npy')
        Y_test = np.load('Y_ltp.npy')
        print('test dataset loaded successfully!')
    os.chdir('../../../')

    X_train = X_train.astype(np.string_)
    arr1 = np.insert(X_train, 19, values=Y_train, axis=1)
    data1 = pd.DataFrame(arr1)
    data1.rename(
        columns={0: 'feature_1', 1: 'feature_2', 2: 'feature_3', 3: 'feature_4', 4: 'feature_5', 5: 'feature_6',
                 6: 'feature_7', 7: 'feature_8', 8: 'feature_9', 9: 'feature_10',
                 10: 'feature_11', 11: 'feature_12', 12: 'feature_13', 13: 'feature_14',
                 14: 'feature_15', 15: 'feature_16', 16: 'feature_17', 17: 'feature_18', 18: 'feature_19', 19: 'grade'},
    inplace=True)
    data1.to_csv('renjiaoban_features.csv')

    X_test = X_test.astype(np.string_)
    arr2 = np.insert(X_test, 19, values=Y_test, axis=1)
    data2 = pd.DataFrame(arr2)
    data2.rename(
        columns={0: 'feature_1', 1: 'feature_2', 2: 'feature_3', 3: 'feature_4', 4: 'feature_5', 5: 'feature_6',
                 6: 'feature_7', 7: 'feature_8', 8: 'feature_9', 9: 'feature_10',
                 10: 'feature_11', 11: 'feature_12', 12: 'feature_13', 13: 'feature_14',
                 14: 'feature_15', 15: 'feature_16', 16: 'feature_17', 17: 'feature_18', 18: 'feature_19', 19: 'grade'},
        inplace=True)
    data2.to_csv('sujiaoban_features.csv')



    print("################################在测试集上进行测试##################################")
    # 对数据进行预处理
    min_max_scalar = preprocessing.MinMaxScaler()
    X_train_scaled = min_max_scalar.fit_transform(X_train)
    X_test_scaled = min_max_scalar.fit_transform(X_test)

    num_splits = 10
    estimator = svm.NuSVC()
    X, Y = shuffle(X_train_scaled, Y_train, random_state=1)

    param_grid = {"nu": [0.25, 0.3, 0.35, 0.4], "kernel": ['rbf', 'poly'],
                  "degree": [1, 2, 3, 4, 5, 6],
                  "gamma": [0.125, 0.25, 0.4, 0.5, 0.6, 0.8, 1, 2, 3, 4, 5]}
    grid = GridSearchCV(estimator=estimator, param_grid=param_grid, scoring='accuracy', cv=num_splits, n_jobs=4)
    grid.fit(X, Y)
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

    Y_true, Y_pred = Y_test, grid.predict(X_test_scaled)
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
    acc = grid.score(X_test_scaled, Y_test)

    class_names = ['lev1', 'lev2', 'lev3', 'lev4', 'lev5']
    print
    print "Detailed classification report:"
    print "The model is trained on the full training set."
    print "The scores are computed on the full test set."
    print classification_report(Y_true, Y_pred, target_names=class_names)
    print "Accuracy:  %.3f" % acc
    print "Error Standard deviation:  %.3f" % err_std
    print

    for i in range(19):
        print "###########################################################################################"
        print("################################在测试集上进行烧灼测试#######################################")
        print("###############################去掉第%d个特征，指标如下######################################" % (i + 1))
        # 对数据进行预处理
        min_max_scalar = preprocessing.MinMaxScaler()
        X_train_scaled = min_max_scalar.fit_transform(X_train)
        X_test_scaled = min_max_scalar.fit_transform(X_test)

        X_train_scaled = np.delete(X_train_scaled, i, axis=1)
        X_test_scaled = np.delete(X_test_scaled, i, axis=1)

        num_splits = 10
        estimator = svm.NuSVC()
        X, Y = shuffle(X_train_scaled, Y_train, random_state=1)

        param_grid = {"nu": [0.25, 0.3, 0.35, 0.4], "kernel": ['rbf', 'poly'],
                      "degree": [1, 2, 3, 4, 5, 6],
                      "gamma": [0.125, 0.25, 0.4, 0.5, 0.6, 0.8, 1, 2, 3, 4, 5]}
        grid = GridSearchCV(estimator=estimator, param_grid=param_grid, scoring='accuracy', cv=num_splits, n_jobs=4)
        grid.fit(X, Y)
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

        Y_true, Y_pred = Y_test, grid.predict(X_test_scaled)
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
        acc = grid.score(X_test_scaled, Y_test)

        class_names = ['lev1', 'lev2', 'lev3', 'lev4', 'lev5']
        print
        print "Detailed classification report:"
        print "The model is trained on the full training set."
        print "The scores are computed on the full test set."
        print classification_report(Y_true, Y_pred, target_names=class_names)
        print "Accuracy:  %.3f" % acc
        print "Error Standard deviation:  %.3f" % err_std
        print
