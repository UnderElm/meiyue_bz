#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/13 8:37 下午
# @Author  : zesen.he
# @File    : main.py
# @Software: PyCharm

from utils import *
import time


def main(target_list, filename):
    exits_song_list = read_exists_songs('exist_song_list.txt')
    print('there are the existed bz list :', exits_song_list)
    for song in target_list:
        if song not in exits_song_list:
            save_dir = '/Users/hezesen/Desktop/Script/meiyue_bz/song_save/{0}/'.format(filename) + song + '/'
            song_file = '{}.mp3'.format(song)
            is_downloaded = False
            try:
                is_downloaded = DownloadFile(get_download_url(get_fst_bz_url(song)), save_dir, song_file)
            except:
                pass
            # 将成功下载的伴奏写入 exist_song_list
            if is_downloaded:
                with open('exist_song_list.txt', 'a') as file:
                    file.write(song +'\n')
            else:
                pass
            time.sleep(5)
        else:
            print(song, ' already exists in list!!!')


if __name__ == '__main__':
    filename = 'song_list'
    song_name_list = []
    with open('{}.txt'.format(filename), 'r') as song_file:
        f = song_file.readlines()
    for line in f:
        song_name_list.append(line.replace('\n',''))
    print('target_bz_list: ',song_name_list)
    main(song_name_list,filename)
