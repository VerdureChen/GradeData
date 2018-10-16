#!usr/bin/env python  
# -*- coding:utf-8 -*-
""" 
@author:nieh 
@file: Features.py 
@time: 2018/03/26 
"""

from __future__ import division
from utils.utils import *
from pyltp import SentenceSplitter
from pyltp import Postagger
from pyltp import Segmentor
from collections import defaultdict
import os
import math
import datetime
import numpy as np


class Feature:
    r"""A list that stores feature values extracted from documents.

    This module is often used to extract feature values from documents stored in a directory, in our case,
    the primary school and junior middle school chinese lexile_fit published by the PEOPLE'S EDUCATION
    PRESS and the JIANGSU EDUCATION PUBLICATION HOUSE. The extracted features values are
    then composed together to form a feature matrix, which can be used to perform a classification
    task using the SVM algorithm.

    Args:
        word_dict (dict): word frequency dictionary created from the SogouW corpus
        char_dict (dict): chinese char frequency dictionary created from the SogouC corpus
        stroke_dict (dict): chinese char stroke dictionary created from Stroke.dat
        path (str): the directory that stores the chinese lexile_fit corpus

    Attributes:
        1. 对数平均词频
        2. 字频1
        3. 字频2
        4. 平均句子长度
        5. 汉字的平均笔画数
        6. 双字词数量
        7. 三字词数量
        8. 四字词数量
        9. 名词数量
        10. 动词数量
        11. 形容词数量
        12. 副词数量
        13. 连词数量
        14. 代词数量
        15. 内容词总数内容词（content word）包括
                    Noun = person, place or thing
                    Verb = action, state
                    Adjective = describes an object, person, place or thing
                    Adverb = tells us how, where or when something happens
        16. 低笔画字数 (1-7)
        17. 中笔画字数 (8-14)
        18. 高笔画字数 (> 14)
        19. 句子数

    """

    def __init__(self, word_dict, char_dict, stroke_dict, path):
        self.word_dict = word_dict
        self.char_dict = char_dict
        self.stroke_dict = stroke_dict
        self.path = path

        LTP_DATA_DIR = '/home1/nh/projects/ltp_data'
        cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
        pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')

        self.segmentor = Segmentor()
        self.segmentor.load(cws_model_path)  # 加载模型

        self.postagger = Postagger()  # 初始化实例
        self.postagger.load(pos_model_path)  # 加载模型

    def features(self, file):
        r"""Extract features from a specified document.

        This method is used to extract features from a specified document and return a list of feature values
        Keyword arguments:
            file -- directory of the document
            thul -- word segmentation mode, loaded once to save time
        """

        term_dict = {}  # 保存分词结果的词项词典
        tag_dict = defaultdict(list)  # {postag: [word1, word2...]}
        num_2char_word = 0  # 双字词数目
        num_3char_word = 0  # 三字词数目
        num_4char_word = 0  # 四字词数目
        num_lowstroke_word = 0  # 低笔画字数
        num_midstroke_word = 0  # 中笔画字数
        num_highstroke_word = 0  # 高笔画字数

        num_chars = count_text_chars(file)  # 文章中的总字数

        # 统计文档中所有汉字的总笔画数
        total_strokes = 0
        with open(file, 'r') as f:
            for line in f:
                ustr = line.decode('utf-8')
                for uchar in ustr:
                    if is_chinese(uchar):
                        char = format(ord(uchar), 'X')
                        total_strokes += self.stroke_dict[char]
                        if self.stroke_dict[char] < 8:
                            num_lowstroke_word += 1
                        elif self.stroke_dict[char] < 15:
                            num_midstroke_word += 1
                        else:
                            num_highstroke_word += 1

        with open(file, 'r') as f:
            str = f.read()
            sents = SentenceSplitter.split(str)
            num_sentences = len(sents)  # 统计文档中的句子数

            words = self.segmentor.segment(str)  # 中文分词
            # segmentor.release()
            word_list = list(words)  # 将分词结果转成列表

            tags = self.postagger.postag(word_list)  # 词性标注
            # postagger.release()

            for tag, word in zip(tags, word_list):
                if tag in tag_dict:
                    tag_dict[tag].append(word)
                else:
                    tag_dict[tag] = [word]

            num_noun = len(tag_dict['n']) + len(tag_dict['nd']) + len(tag_dict['nh']) + len(tag_dict['ni']) + len(
                tag_dict['nl']) + len(tag_dict['ns']) + len(tag_dict['nt']) + len(
                tag_dict['nz'])  # 名词数目 (n -> general noun   nd -> direction noun
            #          nh -> person noun   ni -> organization noun
            #          nl -> location noun  ns -> geographical noun
            #          nt -> temporal noun  nz -> other proper noun)
            num_verb = len(tag_dict['v'])
            num_adj = len(tag_dict['a'])
            num_adv = len(tag_dict['d'])
            num_conj = len(tag_dict['c'])
            num_pronoun = len(tag_dict['r'])
            num_contents = num_noun + num_verb + num_adj + num_adv

            for word in word_list:
                # 分别统计双字词、三字词、四字词数目
                num_chars_per_word = 0  # 词语所含字数
                for uchar in word.decode('utf-8'):
                    if is_chinese(uchar):
                        num_chars_per_word += 1
                    else:
                        break
                if num_chars_per_word == 2:
                    num_2char_word += 1
                elif num_chars_per_word == 3:
                    num_3char_word += 1
                elif num_chars_per_word == 4:
                    num_4char_word += 1

                # 构造分词结果的词项词典
                if word in term_dict:
                    term_dict[word] += 1
                else:
                    term_dict[word] = 1

            val1 = 0
            val2 = 0
            total_freq1 = 0
            total_freq2 = 0
            for word in term_dict:
                if word in self.word_dict:
                    total_freq1 += term_dict[word]
                    val1 += term_dict[word] * math.log(self.word_dict[word], 2)

                if only_chinese(word):
                    if count_str_chars(word) == 1:
                        if word.decode('utf-8') in self.char_dict:
                            total_freq2 += term_dict[word]
                            val2 += term_dict[word] * math.log(self.char_dict[word.decode('utf-8')])

            char_freq_dict = {}
            ustr = str.decode('utf-8')
            for uchar in ustr:
                if is_chinese(uchar):
                    if uchar in char_freq_dict:
                        char_freq_dict[uchar] += 1
                    else:
                        char_freq_dict[uchar] = 1
            total_freq3 = 0
            val3 = 0
            for key in char_freq_dict.iterkeys():
                if key in self.char_dict:
                    if key in self.char_dict:
                        total_freq3 += char_freq_dict[key]
                        val3 += char_freq_dict[key] * math.log(self.char_dict[key], 2)

        if total_freq1 != 0 and total_freq2 != 0 and total_freq3 != 0 and num_sentences != 0 and num_chars != 0:
            avg_wf1 = val1 / total_freq1  # 计算文本的对数平均词频
            avg_wf2 = val2 / total_freq2  # 计算分词结果中单字在参照语料库SogouC中的对数字频对该字在分词结果中字频的加权平均
            avg_wf3 = val3 / total_freq3  # 计算文本中所有汉字在参照语料库SogouC中的对数字频对该字在分词结果中字频的加权平均
            avg_sentence_len = num_chars / num_sentences  # 计算文本的平均句子长度
            avg_strokes = total_strokes / num_chars  # 计算文本的平均笔画数

            print "文章位置%s" % file
            print "(词频，字频1，字频2，句子均长，平均笔画数，双字词数，三字词数， 四字词数， 名词数， 动词数, 形容词数，" \
                  "副词数，连词数，代词数，内容词数，低笔画字数，中笔画字数，高笔画字数，句子数): "

            # print(avg_wf1, avg_wf2, avg_wf3, avg_sentence_len, avg_strokes, num_2char_word, num_3char_word,
            #       num_4char_word, num_noun, num_verb, num_adj, num_adv, num_conj, num_pronoun, num_contents,
            #       num_lowstroke_word, num_midstroke_word, num_highstroke_word, num_sentences)
            feature_list = [avg_wf1, avg_wf2, avg_wf3, avg_sentence_len, avg_strokes, num_2char_word, num_3char_word,
                            num_4char_word, num_noun, num_verb, num_adj, num_adv, num_conj, num_pronoun, num_contents,
                            num_lowstroke_word, num_midstroke_word, num_highstroke_word, num_sentences]
            print(feature_list)
            print

            return feature_list, term_dict  # 特征列表
        else:
            return [], term_dict

    def save_dataset(self):
        # coarse grained features
        # X = []  # 每篇文档的特征向量组成列表
        # Y = []  # 每篇文章所属的类别
        #
        # starttime = datetime.datetime.now()  # 开始时间
        #
        # dirs = os.listdir(self.path)
        # for dir in dirs:
        #     path_to_dir = os.path.join(self.path, dir)
        #     subdirs = os.listdir(path_to_dir)
        #     for subdir in subdirs:
        #         path_to_subdir = os.path.join(path_to_dir, subdir)
        #         if os.path.isdir(path_to_subdir):
        #             for file in os.listdir(path_to_subdir):
        #                 full_filename = os.path.join(path_to_subdir, file)
        #                 feature_list, _ = self.features(full_filename)
        #                 if len(feature_list) != 0:
        #                     X.append(feature_list)
        #                     Y.append(dir)
        #                 else:
        #                     continue
        #         elif os.path.isfile(path_to_subdir):
        #             full_filename = path_to_subdir
        #             feature_list, _ = self.features(full_filename)
        #             if len(feature_list) != 0:
        #                 X.append(feature_list)
        #                 Y.append(dir)
        #             else:
        #                 continue
        # self.segmentor.release()
        # self.postagger.release()
        # endtime = datetime.datetime.now()  # 结束时间
        # print "构造数据集耗时%d秒" % (endtime - starttime).seconds
        #
        # # 得到np.ndarray类型的输入数据集
        # X = np.asarray(X, dtype=np.float64)
        # Y = np.asarray(Y)
        #
        # np.save("X_ltp.npy", X)
        # np.save("Y_ltp.npy", Y)
        # print "dataset saved successfully!"

        # fine grained features
        X = []  # 每篇文档的特征向量组成列表
        Y = []  # 每篇文章所属的类别

        starttime = datetime.datetime.now()  # 开始时间

        dirs = os.listdir(self.path)
        for dir in dirs:
            for file in os.listdir(os.path.join(self.path, dir)):
                full_filename = os.path.join(self.path, dir, file)
                feature_list, _ = self.features(full_filename)
                if len(feature_list) != 0:
                    X.append(feature_list)
                    Y.append(dir)
                else:
                    continue
        endtime = datetime.datetime.now()  # 结束时间
        print "构造数据集耗时%d秒" % (endtime - starttime).seconds

        # 得到np.ndarray类型的输入数据集
        X = np.asarray(X, dtype=np.float64)
        Y = np.asarray(Y)

        np.save("X_ltp.npy", X)
        np.save("Y_ltp.npy", Y)
        print "dataset saved successfully!"
