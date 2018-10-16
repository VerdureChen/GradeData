#!usr/bin/env python  
# -*- coding:utf-8 -*-
""" 
@author:nieh 
@file: GradeDict.py 
@time: 2018/01/26 
"""
import os
import thulac
import sys
import pickle

reload(sys)
sys.setdefaultencoding('utf-8')


class GradeDict:
    """
    统计每个年级课文中的相对增量词汇表
    """

    filepath = ''  # 存放课文的路径

    def __init__(self, filepath):
        self.filepath = filepath

    # 判断一个字符是否是汉字
    def is_chinese(self, uchar):
        """判断一个unicode是否是汉字"""
        if uchar >= u'\u4E00' and uchar <= u'\u9FA5':
            return True
        else:
            return False

    def only_chinese(self, str):
        """判断一个字符串时候只含汉字"""
        term_str = str.decode('utf-8')
        for uterm in term_str:
            if not self.is_chinese(uterm):
                return False
        return True

    def get_vocab(self):
        """根据人教版语文课本语料库构造一年级到九年级的vocabulary"""
        thul = thulac.thulac(seg_only=True)
        dirs = os.listdir(self.filepath)
        dict = {}
        for dir in dirs:
            vocab_set = set()
            path = os.path.join(self.filepath, dir)
            for file in os.listdir(path):
                full_file = os.path.join(path, file)
                with open(full_file, 'r') as f:
                    str = f.read().decode('utf-8')
                    text = thul.cut(str, text=True)
                    seg_list = text.split(' ')
                    for term in seg_list:
                        term = term.encode('utf-8')
                        if self.only_chinese(term):
                            vocab_set.add(term)
            dict[dir] = vocab_set

        list = []
        list.append(dict['one'])
        list.append(dict['two'])
        list.append(dict['three'])
        list.append(dict['four'])
        list.append(dict['five'])
        list.append(dict['six'])
        list.append(dict['seven'])
        list.append(dict['eight'])
        list.append(dict['nine'])
        for i in range(8):
            now_set = set()
            for j in range(i+1):
                now_set = now_set | list[j]
            list[i+1] = list[i+1] - now_set
        a = open("distict_list.pkl", "w")
        pickle.dump(list, a)
        return list
