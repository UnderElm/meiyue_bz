#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/13 8:33 下午
# @Author  : zesen.he
# @File    : uilts.py
# @Software: PyCharm


import requests
from bs4 import BeautifulSoup
import re
import json
import os

# 获得歌曲页面mp3下载链接
def get_download_url(url):
    id = url.rsplit('/', 1)[1].split('.')[0]
    url = 'http://service.5sing.kugou.com/song/getsongurl?songid={}&songtype=bz&from=web'.format(id)
    html = requests.get(url).text[1:-1]
    result = json.loads(html)
    mp3 = result['data']['hqurl']
    if not mp3:
        mp3 = result['data']['lqurl']
    return mp3

# 抓取网页的通用框架,获取页面的内容
def getHtml(url):
    try:
        r = requests.get(url, timeout=30)
        # 状态码不是200就发出httpError的异常
        r.raise_for_status()
        # 获取正确的编码格式
        # r.encoding=r.apparent_encoding
        r.encoding = "utf-8"
        # 打印内容
        return r.text
    except:
        return "wrong!"


# 根据搜索的结果获得第一个伴奏的url
def get_fst_bz_url(name_string):
    url = 'http://search.5sing.kugou.com/?keyword=' + name_string
    html = getHtml(url)
    bs_html = BeautifulSoup(html,'lxml')
    # <script type="text/javascript">
    main_js_text = bs_html.find_all('script')
    try:
        fst_bz_id = re.compile(r"http://5sing.kugou.com/bz/(.*?).html").findall(str(main_js_text).replace('\\',''))[0]
        fst_bz_url = "http://5sing.kugou.com/bz/" + fst_bz_id + ".html"
        print('所爬伴奏主页为： ',fst_bz_url)
        return fst_bz_url
    except:
        raise Exception


# check 歌曲是否已经抓取过，返回一个 歌曲 list
def read_exists_songs(filename):
    exist_song_list = []
    with open(filename, 'r') as exist_file:
        f = exist_file.readlines()
    for line in f:
        exist_song_list.append(line.replace('\n',''))
    return exist_song_list


# 下载框架
def DownloadFile(mp3_url, save_url,file_name):
    try:
        if mp3_url is None or save_url is None or file_name is None:
            print('参数错误')
            return None
        # 文件夹不存在，则创建文件夹
        folder = os.path.exists(save_url)
        if not folder:
            os.makedirs(save_url)
        # 读取MP3资源
        res = requests.get(mp3_url,stream=True)
        # 获取文件地址
        file_path = os.path.join(save_url, file_name)
        print('开始写入文件：', file_path)
        # 打开本地文件夹路径file_path，以二进制流方式写入，保存到本地
        with open(file_path, 'wb') as fd:
            for chunk in res.iter_content():
                fd.write(chunk)
        print(file_name+' 成功下载！')
        return True
    except:
        print("程序错误")
