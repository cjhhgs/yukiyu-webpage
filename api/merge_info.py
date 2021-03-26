import bilibili


def get_bili_info():
    info = bilibili.get_all()
    return info


def merge_info():
    info_list = []
    # append bilibili bangumi below
    bili_list = get_bili_info()
    for i in bili_list:
        info_list.append({'name': i['name'], 'play_url': {'bili': i['play_url']},
                          'episode': i['episode'], 'img': i['img']})
    # bilibili info merge end

    return {'season': info_list}


if __name__ == '__main__':
    info = merge_info()
    print(info)
