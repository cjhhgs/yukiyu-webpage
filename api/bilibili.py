import urllib.request
import os
import json


def url_open(url):
    req = urllib.request.Request(url)
    req.add_header(
        'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    response = urllib.request.urlopen(req)
    html = response.read()
    # buff = BytesIO(html)
    # f = gzip.GzipFile(fileobj=buff)
    return html


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
            bangumi.append({'name': i['title'].replace('/', '-'), 'play_url': i['url'],
                            'episode': i['pub_index'], 'img': i['square_cover']})
    else:
        for i in bangumi_list:
            bangumi.append({'name': i['title'].replace('/', '-'), 'play_url': i['url'],
                            'episode': i['pub_index'], 'img': ""})
    return bangumi


def img_save(bangumi, path):
    rec_path = os.getcwd()
    os.chdir(path)
    for i in bangumi:
        img_url = i['img']
        img_name = i['name']
        # img_path = path+'/'+img_name+'.'+img_url.split('.')[-1]
        img_path = img_name.replace('/', '-')+'.'+img_url.split('.')[-1]
        with open(img_path, 'wb') as f:
            print(img_url)
            img = url_open(img_url)
            f.write(img)
        # img = url_open(img_url)
        # plt.savefig(img_path)
        i['img'] = '../upload/bangumi_img/' + img_path

    os.chdir(rec_path)


def get_all(need_img = False):
    target_url = 'https://bangumi.bilibili.com/web_api/timeline_global'
    # !You should modify this when the working directory changed
    img_folder = os.path.abspath('../upload/bangumi_img')
    apis = api_get(target_url)
    bangumi_list = get_today_list(apis)
    bangumi = get_bangumi(bangumi_list, need_img)
    if need_img == True:
        img_save(bangumi, img_folder)

    return bangumi


if __name__ == '__main__':
    target_url = 'https://bangumi.bilibili.com/web_api/timeline_global'
    # !You should modify this when the working directory changed
    img_folder = os.path.abspath('../upload/bangumi_img')
    apis = api_get(target_url)
    bangumi_list = get_today_list(apis)
    bangumi = get_bangumi(bangumi_list)
    img_save(bangumi, img_folder)
    print(bangumi)
