import urllib.request
import os
import json
import datetime

def url_open(url):
    req = urllib.request.Request(url)
    req.add_header(
        'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    response = urllib.request.urlopen(req)
    html = response.read()
    return html

def get_bangumi_list(html):
    start = html.find('new_anime_list')
    end = html.find(';',start)
    bangumi_list = html[start+17:end]
    bangumi_list = json.loads(bangumi_list)
    # print(type(bangumi_list))
    # print(bangumi_list)
    return bangumi_list

def get_today_bangumi(bangumi_list):
    today = datetime.date.today()
    last_week = str(today + datetime.timedelta(days=-7))
    today = str(today)
    bangumi = []
    # print(bangumi_list)
    for it in bangumi_list:
        if today in it['mtime'] or last_week in it['mtime']:
            bangumi.append({'name':it['name'],'play_url':'https://www.agefans.net/detail/'+it['id'],
                            'episode':it['namefornew'],'img':'../static/upload/default.webp'})
    
    return bangumi

def get_AGE_info(need_img = True):
    target_url = 'https://www.agefans.net/'
    html = url_open(target_url).decode('utf-8')
    bangumi_list = get_bangumi_list(html)
    bangumi = get_today_bangumi(bangumi_list)
    return bangumi

if __name__ == '__main__':
    target_url = 'https://www.agefans.net/'
    html = url_open(target_url).decode('utf-8')
    bangumi_list = get_bangumi_list(html)
    bangumi = get_today_bangumi(bangumi_list)
    print(bangumi)