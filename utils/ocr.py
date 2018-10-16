#!usr/bin/env python  
# -*- coding:utf-8 -*-
""" 
@author:nieh 
@file: ocr.py 
@time: 2018/03/23 
"""

import os
import re
from aip import AipOcr
import time

"""  APPID AK SK """
APP_ID = '10995936'
API_KEY = '4t4l7CNOs1PjL6OZdkieQapi'
SECRET_KEY = 'aKntEukQ8VafSG1i5a48VZfOmucEPxEL'

# """APPID AK SK"""
# APP_ID = '10991992'
# API_KEY = 'ud8KquY9krDOb5g0CPcup8BP'
# SECRET_KEY = 'Gj1qQseYpN5O7n2TNKboBHvEAdhlUHW1'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def save_text(text, path):
    # 将文本内容写入文件
    with open(path, 'w') as fout:
        fout.write(text)  # 3)获取到div标签下的文本内容
        fout.write("\n")


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4E00' and uchar <= u'\u9FA5':
        return True
    else:
        return False


path = "/home1/nh/projects/Readability/sujiaoban_image/"

for dir in os.listdir(path):
    path_to_dir = os.path.join(path, dir)
    subdirs = os.listdir(path_to_dir)
    for subdir in subdirs:
        path_to_subdir = os.path.join(path_to_dir, subdir)
        files = os.listdir(path_to_subdir)
        if not os.path.exists("/home1/nh/projects/Readability/sujiaoban_text/%s/" % dir):
            os.makedirs("/home1/nh/projects/Readability/sujiaoban_text/%s/" % dir)
        os.chdir("/home1/nh/projects/Readability/sujiaoban_text/%s/" % dir)
        text = ''
        num_files = len(files)
        for i in range(1, num_files + 1):
            time.sleep(2)
            image_path = os.path.join(path_to_subdir, '%d.jpg' % i)
            print(image_path)
            try:
                image = get_file_content(image_path)
                # 调用通用文字识别，图片为本地图片
                res = client.basicAccurate(image)
                for item in res['words_result']:
                    text += item['words']

            except KeyError as e:
                print("Error occured...")
                print('error_code', res['error_code'])
                print('error_msg', res['error_msg'])
                exit(1)

        text = re.sub("[\s+/_$%^*(~\"\'`)—\[\]|@<>#【】￥&=（）{}a-zA-Z]", "", text)
        text = text.replace(':', '：')
        text = text.replace('!', '！')
        text = text.replace('?', '？')
        text = text.replace(';', '；')
        text = text.replace(',', '，')
        text = text.replace('…，…', '……')
        text = text.replace('……，', '……')
        text = text.replace('……，', '……')
        text = text.replace('…，，…，', '……')
        text = text.replace('………', '……')
        text = text.replace('......', '……')
        text = text.replace('······', '……')

        num_chars = len(text)
        if is_chinese(text[num_chars - 1]):
            text += '。'
        print(text)
        print()
        save_text(text, subdir)
        os.chdir("../")
