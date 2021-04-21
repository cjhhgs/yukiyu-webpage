# from flaskr.AcFun import get_Ac_info, get_bangumi
import bilibili
import AcFun
import AGE


def get_bili_info(need_img):
    info = bilibili.get_all(need_img)
    return info


def merge_info(need_img = False):
    bangumi_dict={}
    # append bilibili bangumi below
    # info_list = []
    bili_list = get_bili_info(need_img)
    # for i in bili_list:
    #     info_list.append({'name': i['name'], 'play_url': i['play_url'],
    #                       'episode': i['episode'], 'img': i['img']})
    # bilibili info merge end
    bangumi_dict['bilibili']=bili_list

    # append AcFun bangumi below
    ac_list = AcFun.get_Ac_info(need_img)
    bangumi_dict['acfun']=ac_list

    # append AGE bangumi below
    bangumi_dict['AGE'] = AGE.get_AGE_info(True)
    
    return bangumi_dict


if __name__ == '__main__':
    info = merge_info()
    print(info)
