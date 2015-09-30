from hashlib import md5
import base64
import urllib.request
import urllib.parse
import json
import random
import os
import sys

cookie_opener = urllib.request.build_opener()
cookie_opener.addheaders.append(('Cookie', 'appver=2.0.2'))
cookie_opener.addheaders.append(('Referer', 'http://music.163.com'))
urllib.request.install_opener(cookie_opener)

def search_song_by_name(name):
    search_url = 'http://music.163.com/api/search/get'
    params = {
            's': name,
            'type': 1,
            'offset': 0,
            'sub': 'false',
            'limit': 20
    }
    params = urllib.parse.urlencode(params).encode('utf-8')
    resp = urllib.request.urlopen(search_url, params)
    resp_js = json.loads(resp.read().decode('utf-8'))
    if resp_js['code'] == 200 and resp_js['result']['songCount'] > 0:
        result = resp_js['result']
        song_id = result['songs'][0]['id']
        if result['songCount'] > 1:
            for i in range(len(result['songs'])):
                song = result['songs'][i]
                print('[%2d]song:%s\tartist:%s\talbum:%s' % (i+1,song['name'], song['artists'][0]['name'], song['album']['name']))
            select_i = int(input('Select One:'))
            if select_i < 1 or select_i > len(result['songs']):
                print('error select')
                return None
            else:
                song_id = result['songs'][select_i-1]['id']
        detail_url = 'http://music.163.com/api/song/detail?ids=[%d]' % song_id
        resp = urllib.request.urlopen(detail_url)
        song_js = json.loads(resp.read().decode('utf-8'))
        return song_js['songs'][0]
    else:
        return None

def encrypted_id(id):
    print(id)
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
    print(type(result))
    print(result)
    result = result.replace('/', '_')
    result = result.replace('+', '-')
    return result

def save_song_to_disk(song, folder):
    name = song['name']
    fpath = os.path.join(folder, name+'.mp3')
    if os.path.exists(fpath):
        return

    song_dfsId = str(song['bMusic']['dfsId'])
    url = 'http://m%d.music.126.net/%s/%s.mp3' % (random.randrange(1, 3), encrypted_id(song_dfsId), song_dfsId)
    #print '%s\t%s' % (url, name)
    #return
    resp = urllib.request.urlopen(url)
    data = resp.read()
    f = open(fpath, 'wb')
    f.write(data)
    f.close()

def download_song_by_search(name, folder='.'):
    song = search_song_by_name(name)
    if not song:
        print('Not found ' + name)
        return

    if not os.path.exists(folder):
        os.makedirs(folder)
    save_song_to_disk(song, folder)


if __name__ == '__main__':
    download_song_by_search('blue')
