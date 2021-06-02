# A站的爬虫模块
# 从A站中爬取新番数据

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


def img_save(bangumi, path):
    rec_path = os.getcwd()
    os.chdir(path)
    for i in bangumi:
        img_url = i['img']
        if img_url != '../static/upload/default.webp':
            img_name = i['name']
            # img_path = path+'/'+img_name+'.'+img_url.split('.')[-1]
            img_last = img_url.split('.')[-1]
            end = img_last.find("?")
            img_path = img_name.replace('/', '-')+'.'+img_last[0:end]
            print(img_url)
            img = url_open(img_url)
            img = io.BytesIO(img)
            pil_img = Image.open(img)
            img = pil_img.resize((70, 70), Image.ANTIALIAS)
            img.save(img_path)
            i['img'] = '../static/upload/bangumi_img/' + img_path

    os.chdir(rec_path)


def get_bangumi(html, need_img=False):
    today_start = html.find('time-block-active')
    today_end = html.find('</div>', today_start)
    bangumi = []
    # print('start to find from block:')
    # print(html[today_start:today_end])
    # print('\n\n\n')
    start = today_start
    end = today_start
    while end < today_end:
        cur = {}
        start = html.find('list-item', start)
        end = html.find('list-item', start+10)
        # print('find item from:')
        # print(html[start:end])
        # print('\n')
        img_pos = html.find('img src=', start, end)
        start = html.find('a href=', start, end)
        cur_end = html.find('"', start+12, end)
        # print('play_url start = %d, end = %d' %(start,cur_end-1))
        # print('play_url:%s' %(html[start:cur_end-1]))
        cur['play_url'] = 'https://www.acfun.cn' + html[start+9:cur_end-1]
        if need_img:
            # TODO: change this to a default pic
            if img_pos == -1:
                cur['img'] = '../static/upload/default.webp'
            else:
                cur_end = html.find('?', img_pos+10, end)
                cur['img'] = html[img_pos+10:cur_end] + \
                    '?imageView2/1/w/70/h/70'
        else:
            cur['img'] = ''
        start = html.find('<b>', start, end)
        cur_end = html.find('</b>', start, end)
        cur['name'] = html[start+3:cur_end].replace('/', '-').replace("'", " ")
        start = html.find('第', start, end)
        cur_end = html.find('</p>', start, end)
        cur['episode'] = html[start:cur_end].split('>')[-1]
        bangumi.append(cur)
    return bangumi


def get_Ac_info(need_img):
    img_folder = '/home/flask-yukiyu/flaskr/static/upload/bangumi_img/'
    target_url = 'https://www.acfun.cn/?pagelets=pagelet_bangumi_list&pagelets=pagelet_game,pagelet_douga,pagelet_amusement,pagelet_bangumi_list,pagelet_life,pagelet_tech,pagelet_dance,pagelet_music,pagelet_film,pagelet_fishpond,pagelet_sport&reqID=0&ajaxpipe=1&t=1617334393170'
    html = url_open(target_url).decode('utf-8')
    bangumi_list = get_bangumi(html, need_img)
    if need_img == True:
        img_save(bangumi_list, img_folder)
    return bangumi_list


if __name__ == '__main__':
    need_img = False
    img_folder = '/home/flask-yukiyu/flaskr/static/upload/bangumi_img/'
    target_url = 'https://www.acfun.cn/?pagelets=pagelet_bangumi_list&pagelets=pagelet_game,pagelet_douga,pagelet_amusement,pagelet_bangumi_list,pagelet_life,pagelet_tech,pagelet_dance,pagelet_music,pagelet_film,pagelet_fishpond,pagelet_sport&reqID=0&ajaxpipe=1&t=1617334393170'
    html = url_open(target_url).decode('utf-8')
    bangumi_list = get_bangumi(html, need_img)
    if need_img == True:
        img_save(bangumi_list, img_folder)
    print(bangumi_list)
