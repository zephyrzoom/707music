#coding=utf-8

import json
with open(r'E:\m\music_list.json','r+') as f:
    j=json.loads(f.read())
    del(j['music list'][0])
    j['music list'].append({'我哦':'fpaht'})
    print(j)