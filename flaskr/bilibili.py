# B站的爬虫模块
# 从B站中爬取新番数据

from time import sleep
import urllib.request
import os
import json
from PIL import Image
import io


def url_open(url):
    for i in range(10):
        res = try_open(url)
        if res != None:
            return res
        print('request url:%s\nfailed!\nretry after 1 sec!'%url)
        sleep(1)
    
    print('urllib.error.HTTPError: HTTP Error 500: Internal Error')
    return ''.encode('utf-8')


def try_open(url):
    req = urllib.request.Request(url)
    req.add_header(
        'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    try:
        response = urllib.request.urlopen(req)
        html = response.read()
        return html
    except:
        return None

def api_get(url):
    req = urllib.request.Request(url)
    req.add_header(
        'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    response = urllib.request.urlopen(req)
    return json.loads(response.read())


def get_today_list(apis):
    for i in apis['result']:
        # print(i)
        if(i['is_today']):
            return i['seasons']


# we use api to get bangumi list now
def get_bangumi(bangumi_list, need_img):
    bangumi = []
    if need_img == True:
        for i in bangumi_list:
            if 'pub_index' in i:
                bangumi.append({'name': i['title'].replace('/', '-').replace("'", " "), 'play_url': i['url'],
                            'episode': i['pub_index'], 'img': i['square_cover']})
            elif 'delay_reason' in i:
                bangumi.append({'name': i['title'].replace('/', '-').replace("'", " "), 'play_url': i['url'],
                            'episode': i['delay_reason'], 'img': i['square_cover']})
            else:
                bangumi.append({'name': i['title'].replace('/', '-').replace("'", " "), 'play_url': i['url'],
                            'episode': 'unknown', 'img': i['square_cover']})
    else:
        for i in bangumi_list:
            # print(i)
            if 'pub_index' in i:
                bangumi.append({'name': i['title'].replace('/', '-').replace("'", " "), 'play_url': i['url'],
                            'episode': i['pub_index'], 'img': ""})
            elif 'delay_reason' in i:
                bangumi.append({'name': i['title'].replace('/', '-').replace("'", " "), 'play_url': i['url'],
                            'episode': i['delay_reason'], 'img': ""})
            else:
                bangumi.append({'name': i['title'].replace('/', '-').replace("'", " "), 'play_url': i['url'],
                            'episode': 'unknown', 'img': ""})
    return bangumi


def img_save(bangumi, path):
    rec_path = os.getcwd()
    os.chdir(path)
    for i in bangumi:
        img_url = i['img']
        img_name = i['name']
        # img_path = path+'/'+img_name+'.'+img_url.split('.')[-1]
        img_path = img_name.replace('/', '-')+'.'+img_url.split('.')[-1]
        print(img_url)
        img = url_open(img_url)
        img = io.BytesIO(img)
        pil_img = Image.open(img)
        img = pil_img.resize((70,70),Image.ANTIALIAS)
        img.save(img_path)
        i['img'] = '../static/upload/bangumi_img/' + img_path

    os.chdir(rec_path)


def get_all(need_img = False):
    target_url = 'https://bangumi.bilibili.com/web_api/timeline_global'
    # !You should modify this when the working directory changed
    # img_folder = os.path.abspath('../upload/bangumi_img')
    img_folder = '/home/flask-yukiyu/flaskr/static/upload/bangumi_img/'
    apis = api_get(target_url)
    bangumi_list = get_today_list(apis)
    bangumi = get_bangumi(bangumi_list, need_img)
    if need_img == True:
        img_save(bangumi, img_folder)

    return bangumi


if __name__ == '__main__':
    target_url = 'https://bangumi.bilibili.com/web_api/timeline_global'
    # !You should modify this when the working directory changed
    # img_folder = os.path.abspath('../upload/bangumi_img')
    img_folder = '/home/flask-yukiyu/flaskr/static/upload/bangumi_img/'
    apis = api_get(target_url)
    bangumi_list = get_today_list(apis)
    bangumi = get_bangumi(bangumi_list, True)
    img_save(bangumi, img_folder)
    print(bangumi)
