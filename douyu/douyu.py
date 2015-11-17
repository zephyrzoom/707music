#coding=utf-8

import socket
import time
import random
import threading
import re
import json
import sys
import os
import platform
from urllib import request
from tkinter import *
from tkinter import ttk
from html import unescape as unescape_html
import mplay
from tkinter import font
import shutil
from tkinter import messagebox


class my_gui(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.initUI()

        self.g_exit= False


        self.mutex = 0
        self.m_list = {}    # list from search netcloud
        self.selected = False
        #self.FOLD = r'E:\m\music'
        self.FOLD = 'Documents/sublime/danmu_diange/music'







    def initUI(self):
        self.MUSIC_LIST='Documents/sublime/danmu_diange/douyu_0.0.3/music_list.json'
        with open(self.MUSIC_LIST,'r') as f:
            self.play_list = json.loads(f.read())   # list from json
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        mainframe = ttk.Frame(self.root)
        bigFont = font.Font(size=12, weight='bold')
        self.text = Text(mainframe, bg="white", width=50, height=25, state=DISABLED, font=bigFont)
        self.lb_play_list=StringVar()
        self.lb_play_list.set(self.play_list_4_show())
        print(self.play_list)
        self.label = ttk.Label(mainframe, textvariable=self.lb_play_list, font=bigFont, width=20)
        mainframe.grid(column=0,row=0)
        self.text.grid(column=0,row=0)
        self.label.grid(column=1, row=0)



    def write_text(self, nick, content):
        self.text.config(state=NORMAL)
        self.text.insert("end",nick+": "+content+"\n")
        self.text.config(state=DISABLED)
        self.text.yview('end')

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            with open(self.MUSIC_LIST,'w') as f:
                json.dump(self.play_list, f)
            self.root.destroy()



###############################################################################
    def is_exit(self):
        self.g_exit
        return self.g_exit

    """
    calculate the yuwan
    """
    def cast_wetght(self,g):
        g= int(g)
        if g>1e6:
            return str(round(g/1e6,2))+'t'
        elif g>1e3:
            return str(round(g/1e3,2))+'kg'
        else:
            return str(g)+'g'

    """
    s is socket.
    """
    def sendmsg(self,s,msg,code=689):
        data_length= len(msg)+8
        s.send(int.to_bytes(data_length,4,'little'))
        s.send(int.to_bytes(data_length,4,'little'))
        s.send(int.to_bytes(code,4,'little'))
        sent=0
        while sent<len(msg):
            tn= s.send(msg[sent:])
            sent= sent + tn

    def recvmsg(self,s):
        bdata_length= s.recv(12)
        data_length= int.from_bytes(bdata_length[:4],'little')-8
        if data_length<=0:
            print('badlength',bdata_length)
            return None
        total_data=[]
        while True:
            msg= s.recv(data_length)
            if not msg: break
            data_length= data_length - len(msg)
            total_data.append(msg)
        ret= b''.join(total_data)
        return ret

    def unpackage(self,data):
        ret={}
        lines= data.split(b'/')
        lines.pop() # pop b''
        for line in lines:
            kv= line.split(b'@=')
            if len(kv)==2:
                ret[kv[0]]= kv[1].replace(b'@S',b'/').replace(b'@A',b'@')
            else:
                ret[len(ret)]= kv[0].replace(b'@S',b'/').replace(b'@A',b'@')

        return ret

    def unpackage_list(self,l):
        ret=[]
        lines= l.split(b'@S')
        for line in lines:
            line= line.replace(b'@AA',b'')
            mp= line.split(b'@AS')
            tb={}
            for kv in mp:
                try:
                    k,v= kv.split(b'=')
                    tb[k]=v
                except:
                    pass
            ret.append(tb)
        return ret

    def get_longinres(self,s_ip=b'117.79.132.20', s_port=8001, rid=b'265352'):
        s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((s_ip, int(s_port)))

        self.sendmsg(s,b'type@=loginreq/username@=/password@=/roomid@='+rid+b'/\x00')

        #print('==========longinres')
        longinres= self.unpackage(self.recvmsg(s))

        #print('==========msgrepeaterlist')
        msgrepeaterlist= self.unpackage(self.recvmsg(s))
        lst= self.unpackage(msgrepeaterlist[b'list'])
        tb= self.unpackage(random.choice(tuple(lst.values())))

        #print('==========setmsggroup')
        setmsggroup= self.unpackage(self.recvmsg(s))

        ret= {'rid':rid,
              'username': longinres[b'username'],
              'ip': tb[b'ip'],
              'port': tb[b'port'],
              'gid': setmsggroup[b'gid']
             }

        def keepalive_send():
            while not self.is_exit():
                try:
                    self.sendmsg(s,b'type@=keeplive/tick@='+str(random.randint(1,99)).encode('ascii')+b'/\x00')
                except Exception as e:
                    threading.Thread(target=keepalive_send).start()
                time.sleep(45)
            s.close()
        threading.Thread(target=keepalive_send).start()
        def keepalive_recv():
            while not self.is_exit():
                try:
                    bmsg= self.recvmsg(s)
                except Exception as e:
                    threading.Thread(target=keepalive_recv).start()
                #print('*** usr alive:',unpackage(bmsg),'***')
            s.close()
        threading.Thread(target=keepalive_recv).start()
        return ret

    def get_danmu(self,rid=b'5275', ip=b'danmu.douyutv.com', port=8001, username=b'visitor42', gid=b'0'):
        "args needs bytes not str"
        #print('==========danmu')

        s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip,int(port)))
        self.sendmsg(s,b'type@=loginreq/username@='+username+b'/password@=1234567890123456/roomid@='+rid+b'/\x00')
        loginres= self.unpackage(self.recvmsg(s))
        self.sendmsg(s,b'type@=joingroup/rid@='+rid+b'/gid@='+gid+b'/\x00')

        def keepalive():
            while not self.is_exit():
                try:
                    self.sendmsg(s,b'type@=keeplive/tick@='+str(random.randint(1,99)).encode('ascii')+b'/\x00')
                except Exception as e:
                    threading.Thread(target=keepalive).start()
                time.sleep(45)
            s.close()
        threading.Thread(target=keepalive).start()

        while True:
            try:
                bmsg= self.recvmsg(s)
            except Exception as e:
                print('restarting...')
                threading.Thread(target=self.main).start()
                break
            if not bmsg:
                print('*** connection break ***')

            msg= self.unpackage(bmsg)
            msgtype= msg.get(b'type',b'undefined')

            if msgtype==b'chatmessage':
                    nick= msg[b'snick'].decode('utf8')
                    try:
                        content= msg.get(b'content',b'undefined').decode('utf8')
                    except Exception as e:
                        continue
                    print(nick, ':', content)
                    self.analysis_danmu(nick, content)
                    #danmu_play_music.get_music(nick, content)
                    #threading.Thread(target=danmu_play_music.get_music,args=([nick, content]))
                    #notify(nick, content)
            elif msgtype==b'donateres':
                sui= self.unpackage(msg.get(b'sui',b'nick@=undifined//00'))
                nick= sui[b'nick'].decode('utf8')
                #print('***', nick, '送给主播', int(msg[b'ms']),\
                #       '个鱼丸 (', cast_wetght(msg[b'dst_weight']), ') ***')
                #notify(nick, '送给主播' + str(int(msg[b'ms'])) + '个鱼丸')
            elif msgtype==b'keeplive':
                pass
                #print('*** dm alive:',msg,'***')
            elif msgtype in (b'userenter'):
                pass
            else:
                pass
                #print(msg)

    ###########from common.py
    def match1(self,text, *patterns):
        """Scans through a string for substrings matched some patterns (first-subgroups only).

        Args:
            text: A string to be scanned.
            patterns: Arbitrary number of regex patterns.

        Returns:
            When only one pattern is given, returns a string (None if no match found).
            When more than one pattern are given, returns a list of strings ([] if no match found).
        """

        if len(patterns) == 1:
            pattern = patterns[0]
            match = re.search(pattern, text)
            if match:
                return match.group(1)
            else:
                return None
        else:
            ret = []
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    ret.append(match.group(1))
            return ret

    def get_content(self,url, headers={}, decoded=True, cookies_txt=''):
        """Gets the content of a URL via sending a HTTP GET request.

        Args:
            url: A URL.
            headers: Request headers used by the client.
            decoded: Whether decode the response body using UTF-8 or the charset specified in Content-Type.

        Returns:
            The content as a string.
        """

        req = request.Request(url, headers=headers)
        if cookies_txt:
            cookies_txt.add_cookie_header(req)
            req.headers.update(req.unredirected_hdrs)
        response = request.urlopen(req)
        data = response.read()

        # Handle HTTP compression for gzip and deflate (zlib)
        content_encoding = response.getheader('Content-Encoding')
        if content_encoding == 'gzip':
            data = ungzip(data)
        elif content_encoding == 'deflate':
            data = undeflate(data)

        # Decode the response body
        if decoded:
            charset = self.match1(response.getheader('Content-Type'), r'charset=([\w-]+)')
            if charset is not None:
                data = data.decode(charset)
            else:
                data = data.decode('utf-8')

        return data
    ###########from util/strings.py
    # try:
    #   # py 3.4
    #   from html import unescape as unescape_html
    # except ImportError:
    #   import re
    #   from html.entities import entitydefs

    def unescape_html(self, string):
        '''HTML entity decode'''
        string = re.sub(r'&#[^;]+;', _sharp2uni, string)
        string = re.sub(r'&[^;]+;', lambda m: entitydefs[m.group(0)[1:-1]], string)
        return string

    def _sharp2uni(self,m):
        '''&#...; ==> unicode'''
        s = m.group(0)[2:].rstrip(';；')
        if s.startswith('x'):
          return chr(int('0'+s, 16))
        else:
          return chr(int(s))
    ##########

    def get_room_info(self,url):
        #print('==========room')
        html = self.get_content(url)
        room_id_patt = r'"room_id":(\d{1,99}),'
        title_patt = r'<div class="headline clearfix">\s*<h1>([^<]{1,9999})</h1>'
        title_patt_backup = r'<title>([^<]{1,9999})</title>'

        roomid = self.match1(html,room_id_patt)
        title = self.match1(html,title_patt) or self.match1(html,title_patt_backup)
        title = unescape_html(title)

        conf = self.get_content("http://www.douyutv.com/api/client/room/"+roomid)
        metadata = json.loads(conf)
        servers= metadata['data']['servers']
        dest_server= servers[0]
        return {'s_ip': dest_server['ip'],
                's_port': dest_server['port'],
                'rid': metadata['data']['room_id'].encode()
               }
        print(metadata)

    def main(self,url='http://www.douyutv.com/im707'):
        login_user_info= self.get_room_info(url)
        #print('login_user_info:', login_user_info)

        login_room_info= self.get_longinres(**login_user_info)
        #print('login_room_info', login_room_info)
        self.write_text('系统','已启动...')
        self.get_danmu(**login_room_info)


###############################################################################

    def time_count(self,nick, times):
        time.sleep(10)
        #print('系统将在30秒后自动播放第一首')
        for i in range(1, times*10+1):
            if not self.selected:
                time.sleep(0.1)
                count = times*10+1-i
                if count % 100 == 0:
                    self.write_text('系统','将在%d秒之后自动播放第一首歌' % int(count/10))
            else:
                return

        return self.analysis_danmu(nick, '选歌 1')

    def delete_music_start(self):
        path=self.FOLD
        try:
            shutil.rmtree(path)
            os.mkdir(path)
        except Exception as e:
            pass


    def show_music_list(self):
        music_list=self.m_list
        try:
            for i in range(len(music_list['songs'])):
                song = music_list['songs'][i]
                try:
                    self.write_text('系统','[%2d]歌曲:%s\t歌手:%s\t专辑:%s' % (i+1,song['name'], song['artists'][0]['name'], song['album']['name']))
                except Exception as e:
                    self.write_text('系统','[%2d]无法显示该条歌曲信息' % (i+1))
            self.write_text('系统','%s 请尽快选歌' % self.mutex)
        except KeyError as e:
            self.mutex = 0
            self.selected = True
            self.write_text('系统','此歌曲无法显示')
    """分析弹幕

    """
    def analysis_danmu(self, nick, content):
        #self.write_text('测试',str(self.mutex))
        content = content.split(' ')
        if content[0] == '点歌':
            if self.mutex == 0:
                self.mutex = nick
                song_name = ''.join(content[1:])
                self.m_list = mplay.search_song_by_name(song_name)
                if self.m_list == -1:
                    self.mutex = 0
                    self.write_text('系统','%s 没有您要点的歌' % nick)
                else:
                    self.selected = False
                    self.show_music_list()
                    threading.Thread(target=self.time_count, args=([nick, 30])).start()
            elif self.mutex == nick:
                self.selected = True
                song_name = ''.join(content[1:])
                self.m_list = mplay.search_song_by_name(song_name)
                if self.m_list == -1:
                    self.mutex = 0
                    self.write_text('系统','%s 没有您要点的歌' % nick)
                else:
                    self.selected = False
                    self.show_music_list()
                    threading.Thread(target=self.time_count, args=([nick, 30])).start()
            else:
                self.write_text('系统','%s 请等待 %s 点歌' % (nick, self.mutex))
        elif content[0] == '选歌':
            if self.mutex == 0:
                self.write_text('系统','%s 请先点歌' % nick)
            elif self.mutex == nick:
                selected_song = ''.join(content[1:])
                try:
                    selected_song = int(selected_song)
                    song = mplay.select(selected_song, self.m_list)
                    if song != -1:
                        self.selected = True
                        self.mutex = 0
                        music_path = mplay.save_song_to_disk(song, self.FOLD)
                        # add to list
                        print(music_path)
                        print(self.play_list)
                        self.play_list['music list'].append({'id':nick,'mname':song['name'],'mpath':music_path})
                        self.lb_play_list.set(self.play_list_4_show())
                        # with open(self.MUSIC_LIST, 'w') as f:
                        #     json.dump(m_list, f)
                        print(self.play_list['music list'][-1])

                        # with open(self.MUSIC_LIST, 'r') as f:
                        #     m_list = json.loads(f.read())
                        #     self.write_text('song',m_list['music list'][1]['mname'])

                    else:
                        self.write_text('系统','%s 请按照序号选歌' % nick)
                except:
                    self.write_text('系统', '%s 请注意选歌格式' % nick)
            else:
                self.write_text('系统','%s 请等待 %s 选歌' % (nick, self.mutex))
        else:
            pass

    def play_mp3(self):
        while 1:
            while self.play_list['music list']:
                p = mplay.playmp3(self.play_list['music list'][0]['mpath'])
                # while not p.returncode:
                #     print(p)
                #     time.sleep(5)
                self.f5_list()
                self.lb_play_list.set(self.play_list_4_show())  # refresh play list
                print(self.play_list)
            else:
                time.sleep(10)# no music play, wait for sb diange

    def f5_list(self):
        del(self.play_list['music list'][0])

    def play_list_4_show(self):
        tmp_str='  播放列表\n\n'
        for i,v in enumerate(self.play_list['music list']):
            tmp_str=''.join([tmp_str,str(i+1),'. %s:\n  %s' % (v['id'],v['mname']), '\n'])
        return tmp_str

###############################################################################

def maintk():
    root = Tk()
    app = my_gui(root)
    #app.delete_music_start()
    threading.Thread(target=app.main).start()
    threading.Thread(target=app.play_mp3).start()
    #root.after(2000, app.main)
    root.mainloop()



if __name__ == '__main__':
    # url= sys.argv[1] if len(sys.argv)>1 else 'http://www.douyutv.com/im707'
    # #danmu_play_music.delete_music_start()
    # main(url)
    maintk()
