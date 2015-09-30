#coding=utf-8
#author=707

import mplay
import threading
import time
import shutil
import os


"""get music name from the danmu

   return -1: wrong pattern
         str: music name
"""
def get_music_name(content):
    contents = content.split(' ')
    if len(contents) >= 3 and (contents[0] == 'm' or contents[0] == 'M'):
        if contents[1] == 'n' or contents[1] == 'N':
            return ' '.join(contents[2:])
    return -1


"""get select id from the danmu

   return selected: a number > 0
                -1: wrong pattern
"""
def get_select_id(content):
    contents = content.split(' ')
    if len(contents) >= 3 and (contents[0] == 'm' or contents[0] == 'M'):
        if contents[1] == 's' or contents[1] == 'S':
            selected = ''.join(contents[2:])
            try:
                selected = int(selected)
            except Exception as e:
                return -1
            else:
                return selected
    return -1

"""dian ge



"""
mutrex = 0
m_list = {}
selected = False
#FOLD = r'E:\m\music'
FOLD = 'Documents/sublime/danmu_diange/music'
def get_music(nick, content):
    global mutrex
    global selected
    if mutrex == 0:
        m_name = get_music_name(content)
        if m_name != -1:
            mutrex = nick
            global m_list
            m_list = mplay.search_song_by_name(m_name)
            if m_list == -1:
                mutrex = 0
                print('没有要查的歌曲')
            else:
                mplay.show_music_list(m_list)
                selected = False
                threading.Thread(target=time_count, args=([nick, 30])).start()
            return

    elif nick == mutrex:
        m_select = get_select_id(content)
        if m_select != -1:
            selected_song = mplay.select(m_select, m_list)
            if selected_song != -1:
                music_path = mplay.save_song_to_disk(selected_song, FOLD)
                threading.Thread(target=mplay.playmp3, args=([music_path])).start()
                selected = True
            else:
                print('请按照序号选歌')
                return
        else:
            print('请选歌，注意格式，例如想选第一首:m s 1')
            return
        mutrex = 0
    else:
        print('请等待 %s 选歌' % mutrex)


def time_count(nick, times):
    global selected
    time.sleep(10)
    #print('系统将在30秒后自动播放第一首')
    for i in range(1, times*10+1):
        if not selected:
            time.sleep(0.1)
            count = times*10+1-i
            if count % 100 == 0:
                print('系统将在%d秒之后自动播放第一首歌' % int(count/10))
            #print('系统将在%d秒后自动选择第一首歌' % count)
        else:
            return

    # while count < times:
    #     if not selected:
    #         time.sleep(1)
    #         count += 1
    #         print('系统将在%d秒后自动选择第一首歌' % count)
    #     else:
    #         break
    return get_music(nick, 'm s 1')

def delete_music_start(path=FOLD):
    try:
        shutil.rmtree(path)
        os.mkdir(FOLD)
    except Exception as e:
        pass

if __name__=='__main__':
	# login_user_info= douyu.get_room_info(url)
 #    print('login_user_info:', login_user_info)

 #    login_room_info= douyu.get_longinres(**login_user_info)
 #    print('login_room_info', login_room_info)

 #    douyu.get_danmu(**login_room_info)
    pass
