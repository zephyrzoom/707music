#coding=utf-8
from subprocess import Popen
from subprocess import call
import time
import threading

from hashlib import md5
import base64
import urllib.request
import urllib.parse
import json
import random
import os
import sys
import time
import re
import lyric

"""ffplay path
"""
FFMPEG=r'E:\ffmpeg\bin\ffplay.exe'
#FFMPEG='ffplay'

#CLOUDMUSIC=r"E:\Program Files\Netease\CloudMusic\cloudmusic.exe"

"""set cookies
"""
cookie_opener = urllib.request.build_opener()
cookie_opener.addheaders.append(('Cookie', 'appver=2.0.2'))
cookie_opener.addheaders.append(('Referer', 'http://music.163.com'))
urllib.request.install_opener(cookie_opener)

"""search song
@name the name of song
@return dict: including 10 messages at most
        -1: no result by search
"""
def search_song_by_name(name):
    search_url = 'http://music.163.com/api/search/get'
    params = {
            's': name,
            'type': 1,
            'offset': 0,
            'sub': 'false',
            'limit': 10
    }
    params = urllib.parse.urlencode(params).encode('utf-8')
    with urllib.request.urlopen(search_url, params) as resp:
        resp_js = json.loads(resp.read().decode('utf-8'))   # maybe raise an exception
    if resp_js['code'] == 200 and resp_js['result']:
        result = resp_js['result']
        if result['songCount'] > 0:
            return result
            # for i in range(len(result['songs'])):
            #     song = result['songs'][i]
            #     try:
            #     	print('[%2d]歌曲:%s\t歌手:%s\t专辑:%s' % (i+1,song['name'], song['artists'][0]['name'], song['album']['name']))
            #     except Exception as e:
            #     	print('无法显示')
            # print('请选择歌曲m s 序号')
        else:
            return -1
    else:
        return -1

def show_music_list(music_list):
    for i in range(len(music_list['songs'])):
        song = music_list['songs'][i]
        try:
            print('[%2d]歌曲:%s\t歌手:%s\t专辑:%s' % (i+1,song['name'], song['artists'][0]['name'], song['album']['name']))
        except Exception as e:
            print('[%2d]无法显示该条歌曲信息' % (i+1))

"""encode id
"""
def encrypted_id(id):
    byte1 = bytearray('3go8&$8*3*3h0k(2)2', 'utf-8')
    byte2 = bytearray(id, 'utf-8')
    byte1_len = len(byte1)
    for i in range(len(byte2)):
        byte2[i] = byte2[i]^byte1[i%byte1_len]
    m = md5()
    m.update(byte2)

    result = m.digest()
    result = base64.b64encode(result)
    result = str(result, 'utf-8')
    result = result.replace('/', '_')
    result = result.replace('+', '-')
    return result


"""save song
@song song_js['songs'][0..n]
@return -1: romve exception, maybe the file is running
"""
def save_song_to_disk(song, folder):
    name = song['name']
    encode_name = str(random.random())
    fpath = os.path.join(folder, encode_name+'.mp3')
    if os.path.exists(fpath):
        try:
            os.remove(fpath)
        except Exception as e:
            return -1

    print('歌曲加载中...')
    song_dfsId = str(song['bMusic']['dfsId'])
    url = 'http://m%d.music.126.net/%s/%s.mp3' % (random.randrange(1, 3), encrypted_id(song_dfsId), song_dfsId)

    try:
        with urllib.request.urlopen(url) as resp:
            data = resp.read()  # maybe raise an exception
    except Exception as e:
        print('音乐获取失败')
        return -1
    with open(fpath, 'wb') as f:
        f.write(data)
    return fpath
    #threading.Thread(target=playmp3, args=([os.path.join('E:\m\music', name+'.mp3')])).start()


# def download_song_by_search(song, folder='.'):
#     # song = search_song_by_name(name)
#     if not song:
#         print('Not found ' + name)
#         return

#     if not os.path.exists(folder):
#         os.makedirs(folder)
#     save_song_to_disk(song, folder)





"""play the song
if the path is exist
@return -1: no such file
"""
def playmp3(filename):
    if os.path.exists(filename):
        p = Popen([FFMPEG, '-autoexit', filename])
        #p = Popen([CLOUDMUSIC, filename])
        
        #call([FFMPEG, '-autoexit', filename])
        #os.remove(filename)

        return p
    else:
        return -1

"""show menu and select
@id int: ordinal number
@return -1: wrong id
"""

def select(select_id, song_list):
    #print(id, name)
    #resp_js = search_song_by_name(name)
    #result = resp_js['result']
    song_id = song_list['songs'][0]['id']
    #select_i = int(id)
    if select_id < 1 or select_id > len(song_list['songs']):
        return -1
    else:
        song_id = song_list['songs'][select_id-1]['id']
    detail_url = 'http://music.163.com/api/song/detail?ids=[%d]' % song_id
    with urllib.request.urlopen(detail_url) as resp:
        song_js = json.loads(resp.read().decode('utf-8'))
    return song_js['songs'][0],song_id # 音质？

"""切歌
"""
def killu(p):
    p.kill()    #切了之后没有删除歌曲



def getLyric():
    if 'lyric' not in self.songs[str(self.playing_id)].keys():
        self.songs[str(self.playing_id)]["lyric"] = []
    if len(self.songs[str(self.playing_id)]["lyric"]) > 0:
        return
    netease = NetEase()
    lyric = netease.song_lyric(self.playing_id)
    if (not lyric == []) or lyric == '未找到歌词':
        lyric = lyric.split('\n')
    self.songs[str(self.playing_id)]["lyric"] = lyric
    return


def song_lyric(music_id):
    action = "http://music.163.com/api/song/lyric?os=osx&id=" + str(music_id) + "&lv=-1&kv=-1&tv=-1"
    try:
        #params = urllib.parse.urlencode(params).encode('utf-8')
        with urllib.request.urlopen(action) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        if data['lrc']['lyric'] != None:
            lyric_info = data['lrc']['lyric']
            return lyric_info
        else:
            return None
        
    except:
        return None

"""
id:选歌序号
"""
def get_songid(name,selectid):
    mlist=search_song_by_name(name)
    return mlist['songs'][selectid]['id']


if __name__ == '__main__':
    mlist=search_song_by_name('晴天')
    song_id = mlist['songs'][0]['id']
    print(song_id)
    show_music_list(mlist)

    lyric1=song_lyric(song_id)
    print(lyric1)
    l=lyric.Lyric(lyric1)
    l.process_lyric()
    print(l.time_minus)
    print(l.cut_lyric)
    path=save_song_to_disk(select(1,mlist),r'E:\m\music')
    playmp3(path)
    for i in range(len(l.cut_lyric)):
        print(l.cut_lyric[i])
        time.sleep(l.time_minus[i])
        print(l.time_minus[i])

    # lyric.
    # lyric_line=lyric1.split('\n')
    

    # l=lyric.Lyric(lyric_line[4])


    # time_minus=[]
    # lyrics=[]
    # for v in lyric_line:
    #     try:
    #         l=lyric.Lyric(v)
    #         if len(l.millsec)==3:
    #             print(l.millsec)
    #             print(int(l.minite)*60+int(l.sec)+int(l.millsec)/1000)
    #             time_minus.append(int(l.minite)*60+int(l.sec)+int(l.millsec)/1000)
    #         elif len(l.millsec)==2:
    #             time_minus.append(int(l.minite)*60+int(l.sec)+int(l.millsec)/1000)
    #         lyrics.append(l.content)
    #     except Exception as e:
    #         print('error')
    # print(lyrics)
    # print(len(lyrics))
    # for i,v in enumerate(time_minus):
    #     if i<len(time_minus)-1:
    #         time_minus[i]=round(time_minus[i+1]-time_minus[i],3)
    # print(time_minus)
    # print(len(time_minus))