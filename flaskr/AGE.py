import urllib.request
import json
import datetime
from time import sleep

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
            bangumi.append({'name':it['name'].replace('/', '-').replace("'", " "),'play_url':'https://www.agefans.net/detail/'+it['id'],
                            'episode':it['namefornew'],'img':'../static/upload/default.webp'})
    
    return bangumi

def get_AGE_info(need_img = True):
    target_url = 'https://www.agefans.net/'
    html = url_open(target_url).decode('utf-8')
    bangumi_list = get_bangumi_list(html)
    bangumi = get_today_bangumi(bangumi_list)
    return bangumi

if __name__ == '__main__':
    target_url = 'https://agefans.org/'
    html = url_open(target_url).decode('utf-8')
    # bangumi_list = get_bangumi_list(html)
    # bangumi = get_today_bangumi(bangumi_list)
    f = open("age.html", 'w', encoding='utf-8')
    f.write(html)
    print(html)