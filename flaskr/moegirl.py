# 萌娘百科爬虫模块
# 爬取番剧的详细信息
# 包括制作公司、监督、声优等

from time import sleep
import urllib.request
import re

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


def getIndexOfGroup(index, *target):
    for i in target:
        if i != None:
            return i.group(index)
    return ''

def getBangumiInfoList(html):
    html = html[html.find("if (setting.noNumber == \"true\") $('.tocnumber').remove();"):]
    html = html.split('<p><br style="clear:both;" />')

    res = []

    for part in html:
        bangumiName1 = re.search('<h2><span id="(.*?)"></span><span class="mw-headline" id="(.*?)">(.*?)</span></h2>', part)
        bangumiName2 = re.search('<h2><span(.)class="mw-headline" id="(.*?)">(.*?)</span></h2>', part)
        conduct1 = re.search('<li>监督：(.*?)</li>', part)
        conduct2 = re.search('<li>系列监督：(.*?)</li>', part)
        conduct3 = re.search('<li>监督、系列构成：(.*?)</li>', part)
        production1 = re.search('<li>动画制作：(.*?)</li>', part)
        production2 = re.search('<li>制作：(.*?)</li>', part)

        part = part[part.find('CAST'):]
        castRes = re.findall('<li>(.*?)</li>', part)
        # print(castRes)
        cast = []
        for i in castRes:
            cast.append(i.split('：')[-1])

        # print(cast)

        res.append({'name':getIndexOfGroup(3, bangumiName1, bangumiName2),
                    'conduct':getIndexOfGroup(1, conduct1, conduct2, conduct3),
                    'production':getIndexOfGroup(1, production1, production2),
                    'cast':cast})

    # drop the last one because it is unexpected data
    return res[:-1]

def getProduceInfo():
    # target_url = 'https://zh.moegirl.org.cn/%E6%97%A5%E6%9C%AC2021%E5%B9%B4%E6%98%A5%E5%AD%A3%E5%8A%A8%E7%94%BB'
    # html = url_open(target_url).decode('utf-8') 
    html = open('./flaskr/save.txt', encoding='utf-8').read()
    bangumiInfoList = getBangumiInfoList(html)
    print('get bangumiDetailInfo:')
    print(bangumiInfoList)
    return bangumiInfoList

if __name__ == '__main__':
    # target_url = 'https://zh.moegirl.org.cn/%E6%97%A5%E6%9C%AC2021%E5%B9%B4%E5%86%AC%E5%AD%A3%E5%8A%A8%E7%94%BB'
    # html = url_open(target_url).decode('utf-8') 
    # print(html)
    html = open('./flaskr/save.txt', encoding='utf-8').read()
    bangumiInfoList = getBangumiInfoList(html)
    print('get bangumiDetailInfo:')
    print(bangumiInfoList)
    # print(bangumiInfoList)
    # f = open("out.html", "w", encoding='utf-8')  
    # print(html, file=f)