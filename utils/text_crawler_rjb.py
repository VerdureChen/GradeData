#!usr/bin/env python  
# -*- coding:utf-8 -*-
""" 
@author:nieh 
@file: text_crawler_rjb.py
@time: 2018/01/09 
"""
# ---------------------------------------
# 爬取人教版一至九年级语文课本的文本内容
# 保存为文本格式
# ---------------------------------------


import sys
import urllib2
from bs4 import BeautifulSoup
import os

reload(sys)
sys.setdefaultencoding('utf-8')


def crawl_text(url, path):
    # 1)爬取html内容
    html_con = urllib2.urlopen(url).read()

    # 2)获取文本所在的div(使用BeautifulSoup);
    soup = BeautifulSoup(html_con, 'html.parser', from_encoding='utf-8')
    res_post = soup.find('div', class_='ckqw')

    # 将文本内容写入文件
    fout = open(path, 'w')

    fout.write(res_post.get_text().strip())  # 3)获取到div标签下的文本内容
    fout.write("\n")

os.mkdir("renjiaoban")
os.chdir("renjiaoban")

# 爬取一年级的课文
# TODO


# 爬取二年级的课文
os.mkdir("two")
os.chdir("two")
for i in range(34):
    url = "http://www.yuwenziyuan.com/rjb/2s/kewen/" + str(108 - i) + ".html"
    print "从%s处爬取二年级第%i篇课文" % (url, i + 1)
    crawl_text(url, str(i + 1))

for i in range(32):
    url = "http://www.yuwenziyuan.com/rjb/2x/kewen/" + str(140 - i) + ".html"
    print "从%s处爬取二年级第%i篇课文" % (url, i + 35)
    crawl_text(url, str(i + 35))
os.chdir("../")

# 爬取三年级的课文
os.mkdir("three")
os.chdir("three")
for i in range(32):
    url = "http://www.yuwenziyuan.com/rjb/3s/kewen/" + str(495 - i) + ".html"
    print "从%s处爬取三年级第%i篇课文" % (url, i + 1)
    crawl_text(url, str(i + 1))

for i in range(31):
    url = "http://www.yuwenziyuan.com/rjb/3x/kewen/" + str(526 - i) + ".html"
    print "从%s处爬取三年级第%i篇课文" % (url, i + 33)
    crawl_text(url, str(i + 33))
os.chdir("../")

# 爬取四年级的课文
os.mkdir("four")
os.chdir("four")
for i in range(32):
    url = "http://www.yuwenziyuan.com/rjb/4s/kewen/" + str(558 - i) + ".html"
    print "从%s处爬取四年级第%i篇课文" % (url, i + 1)
    crawl_text(url, str(i + 1))

for i in range(32):
    url = "http://www.yuwenziyuan.com/rjb/4x/kewen/" + str(590 - i) + ".html"
    print "从%s处爬取四年级第%i篇课文" % (url, i + 33)
    crawl_text(url, str(i + 33))
os.chdir("../")

# 爬取五年级的课文
os.mkdir("five")
os.chdir("five")
for i in range(28):
    url = "http://www.yuwenziyuan.com/rjb/5s/kewen/" + str(618 - i) + ".html"
    print "从%s处爬取五年级第%i篇课文" % (url, i + 1)
    crawl_text(url, str(i + 1))

for i in range(27):
    url = "http://www.yuwenziyuan.com/rjb/5x/kewen/" + str(645 - i) + ".html"
    print "从%s处爬取五年级第%i篇课文" % (url, i + 28)
    crawl_text(url, str(i + 28))
os.chdir("../")

# 爬取六年级的课文
os.mkdir("six")
os.chdir("six")
for i in range(28):
    url = "http://www.yuwenziyuan.com/rjb/6s/kewen/" + str(673 - i) + ".html"
    print "从%s处爬取六年级第%i篇课文" % (url, i + 1)
    crawl_text(url, str(i + 1))

for i in range(21):
    url = "http://www.yuwenziyuan.com/rjb/6x/kewen/" + str(695 - i) + ".html"
    print "从%s处爬取六年级第%i篇课文" % (url, i + 29)
    crawl_text(url, str(i + 29))
os.chdir("../")

# 爬取七年级的课文
os.mkdir("seven")
os.chdir("seven")
for i in range(30):
    url = "http://www.yuwenziyuan.com/rjb/7s/kewen/" + str(12249 - i) + ".html"
    print "从%s处爬取七年级第%i篇课文" % (url, i + 1)
    crawl_text(url, str(i + 1))

for i in range(30):
    url = "http://www.yuwenziyuan.com/rjb/7x/kewen/" + str(12279 - i) + ".html"
    print "从%s处爬取七年级第%i篇课文" % (url, i + 31)
    crawl_text(url, str(i + 31))
os.chdir("../")

# 爬取八年级的课文
os.mkdir("eight")
os.chdir("eight")
for i in range(30):
    url = "http://www.yuwenziyuan.com/rjb/8s/kewen/" + str(12309 - i) + ".html"
    print "从%s处爬取八年级第%i篇课文" % (url, i + 1)
    crawl_text(url, str(i + 1))

for i in range(30):
    url = "http://www.yuwenziyuan.com/rjb/8x/kewen/" + str(12339 - i) + ".html"
    print "从%s处爬取八年级第%i篇课文" % (url, i + 31)
    crawl_text(url, str(i + 31))
os.chdir("../")

# 爬取九年级的课文
os.mkdir("nine")
os.chdir("nine")
for i in range(25):
    url = "http://www.yuwenziyuan.com/rjb/9s/kewen/" + str(12364 - i) + ".html"
    print "从%s处爬取九年级第%i篇课文" % (url, i + 1)
    crawl_text(url, str(i + 1))

for i in range(23):
    url = "http://www.yuwenziyuan.com/rjb/9x/kewen/" + str(12387 - i) + ".html"
    print "从%s处爬取九年级第%i篇课文" % (url, i + 26)
    crawl_text(url, str(i + 26))
os.chdir("../")




