#!usr/bin/env python  
# -*- coding:utf-8 -*-
""" 
@author:nieh 
@file: util.py
@time: 2018/03/26 
"""

import os
import pickle


def is_chinese(uchar):
    """判断一个unicode字符是否是汉字"""
    if uchar >= u'\u4E00' and uchar <= u'\u9FA5':
        return True
    else:
        return False


def only_chinese(str):
    """判断一个字符串时候只含汉字"""
    term_str = str.decode('utf-8')
    for uterm in term_str:
        if not is_chinese(uterm):
            return False
    return True


def count_str_chars(str):
    """统计字符串所含的汉字数目"""
    num_chars = 0
    ustr = str.decode('utf-8')
    for uchar in ustr:
        if is_chinese(uchar):
            num_chars += 1
    return num_chars


def count_text_chars(file):
    """统计文本所含的汉字数目"""
    num_chars = 0.0  # 文本所有汉字数
    with open(file, 'r') as f:
        for line in f:
            num_chars += count_str_chars(line)
    return num_chars


def construct_dict():
    ref_dir = '/home1/nh/projects/Readability_v2/ref_data'

    # 根据词频文件SogouW.dic文件构造外部词项频率词典
    word_dict = {}
    with open(os.path.join(ref_dir, 'SogouW.dic'), 'r') as f:
        count = 0
        for line in f.readlines():
            line = line.strip()
            if not len(line):
                continue
            line_list = line.split('\t')
            word = line_list[0].decode('gbk', 'ignore').encode('utf-8')
            frequency = int(line_list[1].strip())
            count += 1
            word_dict[word] = frequency

    # 根据外部语料库SogouC构造字频字典，得到语料库中每个字的字频
    dict_path = os.path.join(ref_dir, 'SogouC')
    if os.path.exists('ref_data/dict.pkl'):
        pkl_file = open(os.path.join(ref_dir, 'dict.pkl'), 'rb')
        char_dict = pickle.load(pkl_file)
        pkl_file.close()
    else:
        char_dict = {}
        dirs = os.listdir(dict_path)
        for dir in dirs:
            dir_path = os.path.join(dict_path, dir)
            files = os.listdir(dir_path)
            for file in files:
                full_filename = os.path.join(dir_path, file)
                with open(full_filename, 'r') as f:
                    content = f.read()
                    txt = content.decode('gbk', 'ignore')
                    for uchar in txt:
                        if is_chinese(uchar):
                            char = uchar
                            print char,
                            if char in char_dict:
                                char_dict[char] += 1
                            else:
                                char_dict[char] = 1
        output = open(os.path.join(ref_dir, 'dict.pkl'), 'wb')
        pickle.dump(char_dict, output)
        output.close()

    # 构造汉字笔画词典
    stroke_dict = {}
    with open(os.path.join(ref_dir, 'Stroke.dat'), 'r') as f:
        for line in f.readlines():
            line = line.strip()
            line_list = line.split('\t')
            char = line_list[0]
            stroke = int(line_list[1])
            stroke_dict[char] = stroke
    return word_dict, char_dict, stroke_dict