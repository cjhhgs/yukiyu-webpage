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


if __name__ == '__main__':
    # https://www.acfun.cn/?pagelets=pagelet_bangumi_list&pagelets=pagelet_game,pagelet_douga,pagelet_amusement,pagelet_bangumi_list,pagelet_life,pagelet_tech,pagelet_dance,pagelet_music,pagelet_film,pagelet_fishpond,pagelet_sport&reqID=0&ajaxpipe=1&t=1617334393170
    target_url = 'https://www.acfun.cn/?pagelets=pagelet_bangumi_list&pagelets=pagelet_game,pagelet_douga,pagelet_amusement,pagelet_bangumi_list,pagelet_life,pagelet_tech,pagelet_dance,pagelet_music,pagelet_film,pagelet_fishpond,pagelet_sport&reqID=0&ajaxpipe=1&t=1617334393170'
    html = url_open(target_url).decode('utf-8')
    print(html)