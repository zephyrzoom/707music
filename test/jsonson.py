#coding=utf-8

import json
with open(r'E:\m\music_list.json','r') as f:
    j=json.loads(f.read())
    del(j['music list'][0])
    j['music list'].append({'a':'fpaht'})
    print(j)
with open(r'E:\m\music_list.json','w') as f:
    json.dump(j, r'E:\m\music_list.json')
