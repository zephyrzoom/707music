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
import lyric


class my_gui(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.initUI()

        self.g_exit= False

        self.p=None
        self.mutex = 0
        self.m_list = {}    # list from search netcloud
        self.selected = False
        self.FOLD = r'E:\m\music'
        #self.FOLD = 'Documents/sublime/danmu_diange/music'
        self.VIP_LIST=r'E:\m\douyu_0.0.5\level.json'
        with open(self.VIP_LIST, 'r') as f:
            self.vips = json.loads(f.read())
        self.is_music_play=False
        


    def initUI(self):
        self.MUSIC_LIST=r'E:\m\douyu_0.0.5\music_list.json'
        with open(self.MUSIC_LIST,'r') as f:
            self.play_list = json.loads(f.read())   # list from json
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        mainframe = ttk.Frame(self.root)
        bigFont = font.Font(size=12, weight='bold')
        self.text = Text(mainframe, bg="orange", width=55, height=29, state=DISABLED, font=bigFont)
        self.lb_play_list=StringVar()
        self.lb_play_list.set(self.play_list_4_show())
        self.label = ttk.Label(mainframe, textvariable=self.lb_play_list, font=bigFont, width=20, foreground='blue')
        self.lyric_val=StringVar()
        self.lyric_label=ttk.Label(mainframe, textvariable=self.lyric_val, font=bigFont, padding=10, foreground='red')

        mainframe.grid(column=0,row=0)
        self.text.grid(column=0,row=0)
        self.label.grid(column=1, row=0)
        self.lyric_label.grid(column=0, row=1, columnspan=2)
        self.textcolor='blue'
        

    def change_rand_color(self,position):
        colors=['red','blue','orange','yellow','green','cyan','violet']
        rand_color=random.randint(0,6)
        if position=='字体':
            while self.textcolor==colors[rand_color]:
                rand_color=random.randint(0,6)
            self.textcolor=colors[rand_color]
            while self.textcolor==self.text['bg']:
                rand_color=random.randint(0,6)
                self.textcolor=colors[rand_color]

            self.text['fg']=self.textcolor
        if position=='背景':
            
            while self.text['bg']==colors[rand_color]:
                rand_color=random.randint(0,6)
            self.text['bg']=colors[rand_color]
            while self.text['bg']==self.textcolor:
                rand_color=random.randint(0,6)
                self.text['bg']=colors[rand_color]
            

    def write_text(self, nick, content):
        
        self.text.config(state=NORMAL)
        self.text['fg']=self.textcolor
        self.text.insert("end",nick+": "+content+"\n")
        self.text.config(state=DISABLED)
        self.text.yview('end')

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            with open(self.MUSIC_LIST,'w') as f:
                json.dump(self.play_list, f)
            with open(self.VIP_LIST,'w') as f:
                json.dump(self.vips, f)
            self.root.destroy()



#####################################弹幕#####################################
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

        print('==========longinres')
        longinres= self.unpackage(self.recvmsg(s))

        print('==========msgrepeaterlist')
        msgrepeaterlist= self.unpackage(self.recvmsg(s))
        lst= self.unpackage(msgrepeaterlist[b'list'])
        tb= self.unpackage(random.choice(tuple(lst.values())))

        print('==========setmsggroup')
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
                    print(e)
                    self.write_text('系统','我崩溃了')
                    #threading.Thread(target=self.main).start()
                    exit()
                time.sleep(45)
            s.close()
        threading.Thread(target=keepalive_send).start()
        def keepalive_recv():
            while not self.is_exit():
                try:
                    bmsg= self.recvmsg(s)
                except Exception as e:
                    print(e)
                    self.write_text('系统','我崩溃了')
                    #threading.Thread(target=self.main).start()
                    exit()
                print('*** usr alive:',self.unpackage(bmsg),'***')
            s.close()
        threading.Thread(target=keepalive_recv).start()
        return ret

    def get_danmu(self,rid=b'5275', ip=b'danmu.douyutv.com', port=8001, username=b'visitor42', gid=b'0'):
        "args needs bytes not str"
        print('==========danmu')

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
                    print(e)
                    self.write_text('系统','我崩溃了')
                    #threading.Thread(target=self.main).start()
                    exit()
                time.sleep(45)
            s.close()
        threading.Thread(target=keepalive).start()

        while True:
            try:
                bmsg= self.recvmsg(s)
            except Exception as e:
                print(e)
                self.write_text('系统','我崩溃了')
                #threading.Thread(target=self.main).start()
                exit()
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
                    #print(nick, ':', content)
                    self.analysis_danmu(nick, content)
                    #danmu_play_music.get_music(nick, content)
                    #threading.Thread(target=danmu_play_music.get_music,args=([nick, content]))
                    #notify(nick, content)
            elif msgtype==b'donateres':
                sui= self.unpackage(msg.get(b'sui',b'nick@=undifined//00'))
                nick= sui[b'nick'].decode('utf8')
                # print(self.vips)
                # self.handle_lvl(nick, 10)
                # with open(self.VIP_LIST,'w') as f:
                #     json.dump(self.vips, f)
                # print(self.vips)
                # print(type(nick))
                # print(type(msg[b'ms']))
                print('***', nick, '送给主播', int(msg[b'ms']),\
                       '个鱼丸 (', self.cast_wetght(msg[b'dst_weight']), ') ***')
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
                    self.write_text('系统','将在%d秒之后自动选择第一首歌' % int(count/10))
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
        #print(self.vips)
        #self.write_text('测试',str(self.mutex))
        contents = content.split(' ')
        #print(contents[0],contents[1])
################################################
        if contents[0] == '点歌':
            if len(self.play_list['music list']) < 13:
                #print(self.is_over_diange(nick))
                if not self.is_over_diange(nick):
                    if self.mutex == 0:
                        self.mutex = nick
                        song_name = ''.join(contents[1:])
                        self.m_list = mplay.search_song_by_name(song_name)
                        if self.m_list == -1:
                            self.mutex = 0
                            self.write_text('系统','%s 没有您要点的歌' % nick)
                        else:
                            self.selected = False
                            self.show_music_list()
                            threading.Thread(target=self.time_count, args=([nick, 40])).start()
                    elif self.mutex == nick:
                        self.selected = True
                        song_name = ''.join(contents[1:])
                        self.m_list = mplay.search_song_by_name(song_name)
                        if self.m_list == -1:
                            self.mutex = 0
                            self.write_text('系统','%s 没有您要点的歌' % nick)
                        else:
                            self.selected = False
                            self.show_music_list()
                            threading.Thread(target=self.time_count, args=([nick, 30])).start()
                    else:
                        self.write_text('%s' % self.mutex,'%s 等我选完,我手速慢' % nick)
                else:
                    self.write_text('系统','%s 小伙子 你点的太多了 听听再点' % nick)
            else:
                self.write_text('系统','%s 列表要爆炸了！' % nick)
######################################################
        elif contents[0] == '选歌':
            if self.mutex == 0:
                self.write_text('系统','%s 请先点歌' % nick)
            elif self.mutex == nick:
                selected_song = ''.join(contents[1:])
                try:
                    selected_song = int(selected_song)
                    song,song_id = mplay.select(selected_song, self.m_list)
                    if song != -1:
                        self.selected = True
                        self.mutex = 0
                        self.write_text('系统','%s 正在对选择进行处理...' % nick)
                        music_path = mplay.save_song_to_disk(song, self.FOLD)
                        if music_path != -1:
                            # add to list
                            self.play_list['music list'].append({'id':nick,'mname':song['name'],'mpath':music_path,'sid':song_id})
                            self.lb_play_list.set(self.play_list_4_show())
                            
                            self.write_text('系统','%s 选歌成功 已加入播放列表' % nick)
                            self.handle_lvl(nick,1)
                            with open(self.VIP_LIST,'w') as f:
                                json.dump(self.vips, f)
                        else:
                            self.write_text('系统','%s 歌曲获取失败' % nick)
                    else:
                        self.write_text('系统','%s 请按照序号选歌' % nick)
                except Exception as e:
                    print(e)
                    self.write_text('系统', '%s 请注意选歌格式' % nick)
            else:
                self.write_text('%s' % self.mutex,'%s 等我选完,我手速慢' % nick)
###############################################################
        elif contents[0] == '切歌':
            cut_num = ''.join(contents[1:])
            try:
                cut_num = int(cut_num)
                if cut_num > len(self.play_list['music list']):
                    self.write_text('系统','%s 你瞎啊！' % nick)
                else:
                    cut_nick=self.play_list['music list'][cut_num-1]['id']
                    for i in self.vips['vips']:
                        if cut_nick==i['name']:
                            cut_lvl=self.calc_level(i['lvl'])
                            break
                    for i in self.vips['vips']:
                        if nick == i['name']:
                            lvl = self.calc_level(i['lvl'])
                            break
                    else:
                        lvl = 0

                    if cut_lvl < 2 and nick != cut_nick:
                        self.write_text('%s' % cut_nick,'%s 我才1级,你忍心切我?' % nick)
                    elif cut_lvl >= lvl and nick != cut_nick:
                      
                        self.write_text('%s(%d级)' % (cut_nick,cut_lvl),'%s(%d级) 比我级高才能切哦' % (nick,lvl))
                    else:
                        if cut_num == 1:
                            mplay.killu(self.p)
                            if nick == cut_nick:
                                self.write_text('%s' % nick,'我把自己的歌切了')
                            else:
                                self.write_text('%s' % nick,'%s 我把你的的歌切了,你打我啊' % cut_nick)
                                if lvl-cut_lvl >= 10:
                                    self.write_text('系统','%s 欺负比你低10级以上的小朋友,扣10点经验' % nick)
                                    self.handle_lvl(nick,-10)
                        else:
                            self.f5_list(cut_num-1)
                            self.lb_play_list.set(self.play_list_4_show())
                            if nick == cut_nick:
                                self.write_text('%s' % nick,'我把自己的歌切了')
                            else:
                                self.write_text('%s' % nick,'%s 我把你的的歌切了,你打我啊' % cut_nick)
                                if lvl-cut_lvl >= 10:
                                    self.write_text('系统','%s 欺负比你低10级以上的小朋友,扣掉10点经验' % nick)
                                    self.handle_lvl(nick,-10)
            except Exception as e:
                self.write_text('系统','%s 注意切歌格式' % nick)    
######################################################################

        elif content.strip() == '等级':
            self.write_text('%s' % nick,'我怎么才%d级' % self.get_level(nick))
#####################################################################################
        elif contents[0]=='变色':
            #print(contents[0])
            try:
                contents[1]=''.join(contents[1:]).strip()
                if contents[1]=='字体':
                    self.change_rand_color(contents[1])
                    self.write_text('系统','%s 字体切换成功' % nick)
                elif contents[1]=='背景':
                    self.change_rand_color(contents[1])
                    self.write_text('系统','%s 背景切换成功' % nick)
            except Exception as e:
                self.write_text('系统','%s 注意格式' % nick)
##########################################################################
        elif content.strip() == '经验':
            self.write_text('系统','%s 你的经验值为%d' % (nick,self.get_exp(nick)))
##############################################################################
        elif contents[0]=='赠送':
            try:
                give_nick=contents[1]
                
                if self.is_nick_in_vips(give_nick):
                    
                    try:
                        exp=int(contents[2])
                        if exp >= 0:
                            if self.give_exp(nick,give_nick,exp):
                                with open(self.VIP_LIST,'w') as f:
                                    json.dump(self.vips,f)
                                self.write_text('%s'%nick,'我送给 %s 了%d点经验'%(give_nick,exp))
                            else:
                                self.write_text('系统','%s 小样儿 你经验不够'%nick)
                        else:
                            self.write_text('系统','%s 负的是要抢经验吗?'%nick)
                    except Exception as e:
                        self.write_text('系统','%s 注意经验格式' % nick)
                else:
                    
                    self.write_text('系统','%s 查无此人 让他先点首歌' % give_nick)
            except Exception as e:
                self.write_text('系统','%s 注意格式' % nick)
###############################################################################
        elif content.strip()=='插队':
            if self.get_exp(nick) < 20:
                self.write_text('系统','%s 经验不足20 老实排队吧 插队是壕的游戏' % nick)
            else:
                random_id=[]
                for i,v in enumerate(self.play_list['music list']):
                    if v['id'] == nick and i > 1:
                        random_id.append(i)
                if len(random_id) < 1:
                    self.write_text('系统','%s 你并不能插' % nick)
                else:
                    r=random.randint(0,len(random_id)-1)
                    p1=random_id[r]
                    p2=random.randint(1,p1-1)
                    self.chadui(p1,p2)
                    self.lb_play_list.set(self.play_list_4_show())
                    self.write_text('系统','%s 插队成功' % nick)
                    chadui_exp=random.randint(1,20)
                    self.handle_lvl(nick,-chadui_exp)
                    with open(self.VIP_LIST,'w') as f:
                        json.dump(self.vips, f)
                    self.write_text('系统','%s 插队扣掉%d点经验' % (nick,chadui_exp))
############################################################################
        elif nick == '707472783':
            if contents[0] == '经验':
                try:
                    contents[2] = int(contents[2])
                    self.handle_lvl(contents[1],contents[2])
                    with open(self.VIP_LIST,'w') as f:
                        json.dump(self.vips, f)
                    # with open(r'E:\m\douyu_0.0.5\log.txt','w') as f:
                    #     f.write(' '.join(contents[1],contents[2],'\n'))
                except Exception as e:
                    print('经验值不对')
########################################################################
        else:
            pass

    def play_mp3(self):
        while 1:
            while self.play_list['music list']:
                self.is_music_play=True
                threading.Thread(target=self.show_lyric).start()
                self.p = mplay.playmp3(self.play_list['music list'][0]['mpath'])
                
                self.p.wait()
                self.is_music_play=False
                self.f5_list()
                self.lb_play_list.set(self.play_list_4_show())  # refresh play list
                time.sleep(3)
                #print(self.play_list)
            else:
                time.sleep(10)# no music play, wait for sb diange

    def f5_list(self,num=0):
        del(self.play_list['music list'][num])

    def chadui(self,p1,p2):
        self.play_list['music list'].insert(p2,self.play_list['music list'][p1])
        del(self.play_list['music list'][p1+1])
        
    def play_list_4_show(self):
        tmp_str='  播放列表\n\n'
        for i,v in enumerate(self.play_list['music list']):
            tmp_str=''.join([tmp_str,str(i+1),'. %s:\n   %s' % (v['id'],v['mname']), '\n'])
        return tmp_str

    def get_exp(self,nick):
        for i in self.vips['vips']:
            if nick == i['name']:
                return i['lvl']
        else:
            return 0

    def get_level(self,nick):
        for i in self.vips['vips']:
            if nick == i['name']:
                return self.calc_level(i['lvl'])
        else:
            return 0

    def calc_level(self,lvl):
        start=1
        MAX=1000
        while start < MAX:
            lvl_value=(start*(start+1))/2
            if lvl < lvl_value:
                return start-1
            else:
                start += 1
        else:
            self.write_text('系统','等级已到上限')
            return -1

    def write_level(self,nick,lvl):
        for i in self.vips['vips']:
            if i['name'] == nick:
                i['lvl'] += lvl
                break
        else:
            self.vips['vips'].append({'name':nick,'lvl':lvl})

    def handle_lvl(self,nick, exp):
        lvl = self.get_level(nick)
        self.write_level(nick,exp)   #100鱼丸=10点经验
        after_lvl=self.get_level(nick)
        if after_lvl > lvl:
            self.write_text('%s' % nick,'我终于升到%d级了' % after_lvl)


    def show_lyric(self):
        # name=self.play_list['music list'][0]['mname']
        # selectid=self.play_list['music list'][0]['sid']
        # print('sid:',selectid)
        # songid=mplay.get_songid(name,selectid-1)
        # print('songid:',songid)
        songid=self.play_list['music list'][0]['sid']
        getlyric=mplay.song_lyric(songid)
        #print(getlyric)
        if getlyric != None:
            l = lyric.Lyric(getlyric)
            l.process_lyric()
            #print(l.time_minus)
            self.lyric_val.set(getlyric)
            #print(name,selectid,songid,l.time_minus,l.cut_lyric)
            for i in range(len(l.cut_lyric)):
                if self.is_music_play:
                    #print(l.cut_lyric[i])
                    #print(l.time_minus[i])
                    self.lyric_val.set(l.cut_lyric[i])
                    time.sleep(l.time_minus[i])
                else:
                    self.lyric_val.set('')
                    return
            else:
                self.lyric_val.set('')
        else:
            self.lyric_val.set('无歌词')

    """列表中的歌是否超过3首
    """
    def is_over_diange(self,nick):
        count=0
        for i in self.play_list['music list']:
            # print(i['mname'])
            # print(count)
            if nick == i['id']:
                count += 1

        if count >= 3:
            return True
        else:
            return False

    """送经验
    return False:经验不够
    """
    def give_exp(self,nick,give_nick,exp):
        origin_exp=self.get_exp(nick)
        if origin_exp<exp:
            return False
        else:
            self.handle_lvl(nick,-exp)
            self.handle_lvl(give_nick,exp)
            return True

    """名字是否在列表中
    """
    def is_nick_in_vips(self, nick):
        for i in self.vips['vips']:
            if nick == i['name']:
                return True
        else:
            return False


###############################################################################

def maintk():
    root = Tk()
    app = my_gui(root)
    #app.write_text('wo','wo')
    #app.delete_music_start()

    threading.Thread(target=app.main).start()
    threading.Thread(target=app.play_mp3).start()
    root.mainloop()



if __name__ == '__main__':
    # url= sys.argv[1] if len(sys.argv)>1 else 'http://www.douyutv.com/im707'
    # #danmu_play_music.delete_music_start()
    # main(url)

    maintk()
    
