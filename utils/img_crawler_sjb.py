#!usr/bin/env python  
# -*- coding:utf-8 -*-
""" 
@author:nieh 
@file: img_crawler_sjb.py
@time: 2018/01/09 
"""
# ---------------------------------------
# 爬取苏教版一至九年级语文课本的扫描图片
# 保存为jpg格式
# ---------------------------------------


import sys
import urllib2
import urllib
import os
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')


def find_images(url, img_path):
    """
    找到图片的源地址
    :param url:
    :return:
    """

    # 获取当前html页面的内容
    html = urllib2.urlopen(url)
    html_con = html.read()
    html.close()

    # 获取图片所在的div
    soup = BeautifulSoup(html_con, 'html.parser')
    res_post = soup.find('div', class_='dzkb')
    imag = res_post.find('img')
    imag_link = imag.get('src')

    # 将图片按照指定的文件名保存
    urllib.urlretrieve(imag_link, img_path)


def get_remaining_imgs(url):
    """
    找到当前页面下所有的下一页链接
    :param url:
    :return:
    """

    # 获取当前html页面的内容
    print url
    html = urllib2.urlopen(url)
    html_con = html.read()
    html.close()

    soup = BeautifulSoup(html_con, 'html.parser')
    res_post = soup.find('div', class_='ckqw')

    links = res_post.find_all('a')
    if len(links) != 0:
        links.pop()

        sub_link = url.split('/').pop()

        # 将各个子链接下的课文图片爬取，并保存为jpg格式
        j = 2
        for next_link in links:
            str = next_link.get('href').encode('unicode-escape').decode('string_escape')
            next_url = url.replace(sub_link, str)
            print next_url
            find_images(next_url, '%i.jpg' % j)
            j += 1


os.mkdir("sujiaoban")
os.chdir("sujiaoban")

# 爬取一年级上的课文图片
# TODO

# 爬取一年级下的课文图片
# TODO

# 爬取二年级上的课文图片
os.mkdir("2上")
os.chdir("2上")
print "下载2上："
for i in range(23):
    os.mkdir("%i" % (i + 1))
    os.chdir("%i" % (i + 1))
    url = "http://www.yuwenziyuan.com/sjb/2s/dzkb/" + str(23607 + i) + ".html"
    print "正在下载第%i篇课文的图片" % (i + 1)
    find_images(url, "1.jpg")
    get_remaining_imgs(url)

    os.chdir("../")
os.chdir("../")

# 爬取二年级下的课文图片
os.mkdir("2下")
os.chdir("2下")
print "下载2下："
for i in range(24):
    os.mkdir("%i" % (i + 1))
    os.chdir("%i" % (i + 1))
    url = "http://www.yuwenziyuan.com/sjb/2x/dzkb/" + str(23633 + i) + ".html"
    print "正在下载第%i篇课文的图片" % (i + 1)
    find_images(url, "1.jpg")
    get_remaining_imgs(url)

    os.chdir("../")
os.chdir("../")

# 爬取三年级上的课文图片
os.mkdir("3上")
os.chdir("3上")
print "下载3上："
for i in range(24):
    os.mkdir("%i" % (i + 1))
    os.chdir("%i" % (i + 1))
    url = "http://www.yuwenziyuan.com/sjb/3s/dzkb/" + str(23659 + i) + ".html"
    print "正在下载第%i篇课文的图片" % (i + 1)
    find_images(url, "1.jpg")
    get_remaining_imgs(url)

    os.chdir("../")
os.chdir("../")

# 爬取三年级下的课文图片
os.mkdir("3下")
os.chdir("3下")
print "下载3下："
for i in range(26):
    os.mkdir("%i" % (i + 1))
    os.chdir("%i" % (i + 1))
    url = "http://www.yuwenziyuan.com/sjb/3x/dzkb/" + str(23687 + i) + ".html"
    print "正在下载第%i篇课文的图片" % (i + 1)
    find_images(url, "1.jpg")
    get_remaining_imgs(url)

    os.chdir("../")
os.chdir("../")

# 爬取四年级上的课文图片
os.mkdir("4上")
os.chdir("4上")
print "下载4上："
for i in range(25):
    os.mkdir("%i" % (i + 1))
    os.chdir("%i" % (i + 1))
    url = "http://www.yuwenziyuan.com/sjb/4s/dzkb/" + str(23716 + i) + ".html"
    print "正在下载第%i篇课文的图片" % (i + 1)
    find_images(url, "1.jpg")
    get_remaining_imgs(url)

    os.chdir("../")
os.chdir("../")

# 爬取四年级下的课文图片
os.mkdir("4下")
os.chdir("4下")
print "下载4下："
for i in range(23):
    os.mkdir("%i" % (i + 1))
    os.chdir("%i" % (i + 1))
    url = "http://www.yuwenziyuan.com/sjb/4x/dzkb/" + str(23743 + i) + ".html"
    print "正在下载第%i篇课文的图片" % (i + 1)
    find_images(url, "1.jpg")
    get_remaining_imgs(url)

    os.chdir("../")
os.chdir("../")

# 爬取五年级上的课文图片
os.mkdir("5上")
os.chdir("5上")
print "下载5上："
for i in range(26):
    os.mkdir("%i" % (i + 1))
    os.chdir("%i" % (i + 1))
    url = "http://www.yuwenziyuan.com/sjb/5s/dzkb/" + str(23770 + i) + ".html"
    print "正在下载第%i篇课文的图片" % (i + 1)
    find_images(url, "1.jpg")
    get_remaining_imgs(url)

    os.chdir("../")
os.chdir("../")

# 爬取五年级下的课文图片
os.mkdir("5下")
os.chdir("5下")
print "下载5下："
for i in range(28):
    os.mkdir("%i" % (i + 1))
    os.chdir("%i" % (i + 1))
    url = "http://www.yuwenziyuan.com/sjb/5x/dzkb/" + str(23798 + i) + ".html"
    print "正在下载第%i篇课文的图片" % (i + 1)
    find_images(url, "1.jpg")
    get_remaining_imgs(url)

    os.chdir("../")
os.chdir("../")

# 爬取六年级上的课文图片
os.mkdir("6上")
os.chdir("6上")
print "下载6上："
for i in range(26):
    os.mkdir("%i" % (i + 1))
    os.chdir("%i" % (i + 1))
    url = "http://www.yuwenziyuan.com/sjb/6s/dzkb/" + str(23827 + i) + ".html"
    print "正在下载第%i篇课文的图片" % (i + 1)
    find_images(url, "1.jpg")
    get_remaining_imgs(url)

    os.chdir("../")
os.chdir("../")

# 爬取六年级下的课文图片
os.mkdir("6下")
os.chdir("6下")
print "下载6下："
for i in range(25):
    os.mkdir("%i" % (i + 1))
    os.chdir("%i" % (i + 1))
    url = "http://www.yuwenziyuan.com/sjb/6x/dzkb/" + str(23856 + i) + ".html"
    print "正在下载第%i篇课文的图片" % (i + 1)
    find_images(url, "1.jpg")
    get_remaining_imgs(url)

    os.chdir("../")
os.chdir("../")

# 爬取七年级上的课文图片
os.mkdir("7上")
os.chdir("7上")
print "下载7上："
for i in range(54):
    os.mkdir("%i" % (i + 1))
    os.chdir("%i" % (i + 1))
    url = "http://www.yuwenziyuan.com/sjb/7s/dzkb/" + str(23885 + i) + ".html"
    print "正在下载第%i篇课文的图片" % (i + 1)
    find_images(url, "1.jpg")
    get_remaining_imgs(url)

    os.chdir("../")
os.chdir("../")

# 爬取七年级下的课文图片
os.mkdir("7下")
os.chdir("7下")
print "下载7下："
for i in range(53):
    os.mkdir("%i" % (i + 1))
    os.chdir("%i" % (i + 1))
    url = "http://www.yuwenziyuan.com/sjb/7x/dzkb/" + str(23943 + i) + ".html"
    print "正在下载第%i篇课文的图片" % (i + 1)
    find_images(url, "1.jpg")
    get_remaining_imgs(url)

    os.chdir("../")
os.chdir("../")

# 爬取八年级上的课文图片
os.mkdir("8上")
os.chdir("8上")
print "下载8上："
for i in range(44):
    os.mkdir("%i" % (i + 1))
    os.chdir("%i" % (i + 1))
    url = "http://www.yuwenziyuan.com/sjb/8s/dzkb/" + str(24062 + i) + ".html"
    print "正在下载第%i篇课文的图片" % (i + 1)
    find_images(url, "1.jpg")
    get_remaining_imgs(url)

    os.chdir("../")
os.chdir("../")

# 爬取八年级下的课文图片
os.mkdir("8下")
os.chdir("8下")
print "下载8下："
for i in range(54):
    os.mkdir("%i" % (i + 1))
    os.chdir("%i" % (i + 1))
    url = "http://www.yuwenziyuan.com/sjb/8x/dzkb/" + str(24002 + i) + ".html"
    print "正在下载第%i篇课文的图片" % (i + 1)
    find_images(url, "1.jpg")
    get_remaining_imgs(url)

    os.chdir("../")
os.chdir("../")

# 爬取九年级上的课文图片
os.mkdir("9上")
os.chdir("9上")
print "下载9上："
for i in range(43):
    os.mkdir("%i" % (i + 1))
    os.chdir("%i" % (i + 1))
    url = "http://www.yuwenziyuan.com/sjb/9s/dzkb/" + str(24110 + i) + ".html"
    print "正在下载第%i篇课文的图片" % (i + 1)
    find_images(url, "1.jpg")
    get_remaining_imgs(url)

    os.chdir("../")
os.chdir("../")

# 爬取九年级下的课文图片
os.mkdir("9下")
os.chdir("9下")
print "下载9下："
for i in range(30):
    os.mkdir("%i" % (i + 1))
    os.chdir("%i" % (i + 1))
    url = "http://www.yuwenziyuan.com/sjb/9x/dzkb/" + str(24160 + i) + ".html"
    print "正在下载第%i篇课文的图片" % (i + 1)
    find_images(url, "1.jpg")
    get_remaining_imgs(url)

    os.chdir("../")
os.chdir("../")
