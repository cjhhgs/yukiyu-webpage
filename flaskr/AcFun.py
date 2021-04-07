import urllib.request
import os
import json
# from PIL import Image
import io

def url_open(url):
    req = urllib.request.Request(url)
    req.add_header(
        'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    response = urllib.request.urlopen(req)
    html = response.read()
    return html

def get_bangumi(html, need_img=False):
    today_start = html.find('time-block-active')
    today_end = html.find('</div>', today_start)
    bangumi = []
    start = today_start
    end = today_start
    while end < today_end:
        cur = {}
        start = html.find('list-item', start)
        end = html.find('list-item',start+10)
        img_pos = html.find('img src=', start,end)
        start = html.find('a href=', start,end)
        cur_end = html.find('"', start+12,end)
        # print('play_url start = %d, end = %d' %(start,cur_end-1))
        # print('play_url:%s' %(html[start:cur_end-1]))
        cur['play_url'] = 'https://www.acfun.cn' + html[start+8:cur_end-1]
        if need_img:
            # TODO: change this to a default pic 
            if img_pos == -1:
                cur['img'] = '../static/upload/default.webp'
            else:
                cur_end=html.find('?',img_pos+10,end)
                cur['img'] = html[img_pos+10:cur_end] + '?imageView2/1/w/70/h/70'
        else:
            cur['img'] = ''
        start = html.find('<b>',start,end)
        cur_end = html.find('</b>',start,end)
        cur['name'] = html[start+3:cur_end]
        start = html.find('第',start,end)
        cur_end = html.find('</p>',start,end)
        cur['episode'] = html[start:cur_end]
        bangumi.append(cur)
    return bangumi

def get_Ac_info(need_img):
    target_url = 'https://www.acfun.cn/?pagelets=pagelet_bangumi_list&pagelets=pagelet_game,pagelet_douga,pagelet_amusement,pagelet_bangumi_list,pagelet_life,pagelet_tech,pagelet_dance,pagelet_music,pagelet_film,pagelet_fishpond,pagelet_sport&reqID=0&ajaxpipe=1&t=1617334393170'
    html = url_open(target_url).decode('utf-8')
    bangumi_list = get_bangumi(html,need_img)
    return bangumi_list

if __name__ == '__main__':
    # https://www.acfun.cn/?pagelets=pagelet_bangumi_list&pagelets=pagelet_game,pagelet_douga,pagelet_amusement,pagelet_bangumi_list,pagelet_life,pagelet_tech,pagelet_dance,pagelet_music,pagelet_film,pagelet_fishpond,pagelet_sport&reqID=0&ajaxpipe=1&t=1617334393170
    target_url = 'https://www.acfun.cn/?pagelets=pagelet_bangumi_list&pagelets=pagelet_game,pagelet_douga,pagelet_amusement,pagelet_bangumi_list,pagelet_life,pagelet_tech,pagelet_dance,pagelet_music,pagelet_film,pagelet_fishpond,pagelet_sport&reqID=0&ajaxpipe=1&t=1617334393170'
    html = url_open(target_url).decode('utf-8')
    bangumi_list = get_bangumi(html,True)
    print(bangumi_list)