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

# this is for html sorce code
# def get_bangumi(html):
#     bangumi = []
#     cur_group_start = html.find('season-group is-published today')
#     cur_group_end = html.find('season-group is-published today', cur_group_start)
#     while cur_group_end != -1:
#         # get detail info of each bangumi
#         start = html.find('season-item',cur_group_start,cur_group_end)
#         end = html.find('season-item',start,cur_group_end)
#         while start != -1:
#             play_url_start=('//www.bilibili.com/bangumi/play/', start, end)
#             play_url_end=('"',play_url_start,end)
#             play_url = html[play_url_start:play_url_end]
#             name_start=html.find('title=',play_url_end,end) + 7
#             name_end=html.find('"',name_start,end)
#             bangumi_name=html[name_start,name_end]
#             episode_start = html.find('season-desc published',name_end,end) + 24
#             episode_end = html.find('</div>',episode_start,end)
#             episode = html[episode_start:episode_end]
#             # store the info of one bangumi
#             bangumi.append([bangumi_name,play_url,episode])
#             start = html.find('season-item',end,cur_group_end)
#             end = html.find('season-item',start,cur_group_end)
#     return bangumi

# we use api to get bangumi list now


def get_bangumi(bangumi_list):
    bangumi = []
    for i in bangumi_list:
        bangumi.append({'name': i['title'], 'play_url': i['url'],
                        'episode': i['pub_index'], 'img': i['square_cover']})
    return bangumi


def img_save(bangumi, path):
    os.chdir(path)
    for i in bangumi:
        img_url = i['img']
        img_name = i['name']
        # img_path = path+'/'+img_name+'.'+img_url.split('.')[-1]
        img_path = img_name.split('/')[0]+'.'+img_url.split('.')[-1]
        with open(img_path, 'wb') as f:
            print(img_url)
            img = url_open(img_url)
            f.write(img)
        img = url_open(img_url)
        # plt.savefig(img_path)
        i['img'] = '../upload/bangumi_img/' + img_path


if __name__ == '__main__':
    target_url = 'https://bangumi.bilibili.com/web_api/timeline_global'
    # !You should modify this when the working directory changed
    img_folder = os.path.abspath('../upload/bangumi_img')
    apis = api_get(target_url)
    bangumi_list = get_today_list(apis)
    bangumi = get_bangumi(bangumi_list)
    img_save(bangumi, img_folder)
    print(bangumi)
