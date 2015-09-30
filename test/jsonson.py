#coding=utf-8

import json
PATH='list.json'
with open(PATH,'r') as f:
    j=json.loads(f.read())
    del(j['music list'][0])
    j['music list'].append({'a':'fpaht'})
    print(j)
with open(PATH,'w') as f:
    json.dump(j, f)
