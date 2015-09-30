#coding=utf-8
from tkinter import *
from tkinter import ttk
from tkinter import font
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
import danmu_play_music


class ClassName(object):
    """docstring for ClassName"""
    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg
        
root = Tk()
mainframe = ttk.Frame(root, padding=(3,3,12,12), width=800, height=600)
mainframe.grid(column=0,row=0,sticky=(N, W, E, S))

bigFont = font.Font(size=18, weight='bold')
info_title = ttk.Label(mainframe, text='点歌方法', font=bigFont, foreground='red').grid(column=0, row=0)
info1 = ttk.Label(mainframe, text='1.点歌:m n 歌名', font=bigFont, foreground='red').grid(column=0, row=1, sticky=(W))
info2 = ttk.Label(mainframe, text='2.选歌:m s 序号', font=bigFont, foreground='red').grid(column=0, row=2, sticky=(W))
info3 = ttk.Label(mainframe, text='注意两处空格', font=bigFont, foreground='red').grid(column=0, row=4, sticky=(W))
info3 = ttk.Label(mainframe, text='手滑的朋友看这里：', font=bigFont).grid(column=0, row=5, sticky=(W))
info4 = ttk.Label(mainframe, text='m n 南山南', font=bigFont).grid(column=0, row=6, sticky=(W))
info5 = ttk.Label(mainframe, text='m s 1', font=bigFont).grid(column=0, row=7, sticky=(W))

shell = StringVar()


console = ttk.Label(mainframe, textvariable=shell)
console.grid(column=2, row=0, rowspan=20)

music_list = StringVar()
mlist = ttk.Label(mainframe, textvariable=music_list).grid(column=3, row=0, rowspan=20)
music_list.set('mlist')
def set_console(content):
    global shell
    shell.set(content)

root.mainloop()


    