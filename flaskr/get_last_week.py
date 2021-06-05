# 获取数据库中最近一周的番剧信息接口
# 该模块提供了返回最近一周番剧信息的函数
# 为前端数据展示API提供调用

import pymysql
import datetime
from databaseCURD import signColumnsShuffle

# via veiw to get the detail info of a target bangumi
def get_detail_info(id='4100450'):
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    print('get bangumi detail info: ')
    cursor = db.cursor()
    sql = """
        select * from detail_info
        where bangumi_id = %s
        """%id
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    sql = """
        select actor from bangumi_cast
        where bangumi_id = %s
        """%id
    cursor.execute(sql)
    cast = cursor.fetchall()
    cast = signColumnsShuffle(cast)
    print(cast)
    res = {'result': None}
    if data and cast:
        data = data[0]
        res['result'] = {
            'id':  data[0],
            'name': data[1],
            'company_name': data[2],
            'conduct_name': data[3],
            'img': data[4],
            'cast': cast
        }
    return res

def get_list_of_date(day, target_table):
    # date = day.strftime("%Y-%m-%d")
    date = day
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    cursor = db.cursor(pymysql.cursors.DictCursor)  #返回值为字典格式
    sql1 = """
        select  bangumi_id, name, img, play_url, episode
        from    bangumi_list natural join %s
        where   last_update = '%s'
        """% \
        (target_table, date)
    cursor.execute(sql1)
    data = cursor.fetchall()    #列表
    cursor.close()
    db.close()

    return data
            

def get_target_week(netName):
    today = datetime.date.today()
    bangumi_list = list()
    for i in range(0,7):
        last_day = today + datetime.timedelta(days= -i)
        weekday = last_day.weekday()
        date = last_day.strftime("%Y-%m-%d")
        list_of_day = get_list_of_date(last_day, netName)
        # solve mysql return void tuble when it is null
        if type(list_of_day) == type(()):
            list_of_day = []
        # update the play_url, make it become a dict
        for i in list_of_day:
            i['play_url'] = {netName: i['play_url']}
        temp = {"date":date,"weekday":weekday,"seasons":list_of_day}
        bangumi_list.append(temp)
    return sorted(bangumi_list, key=lambda keys: keys["weekday"])

def merge_seasons(left, right, right_name):
    for i in right:
        flag = True
        for k in left:
            # if find in left dict
            if i['bangumi_id']==k['bangumi_id']:
                k['play_url'][right_name] = i['play_url'][right_name]
                flag = False
        # if not find in left dict, appent new
        if flag == True:
            left.append(i)

def merge_list(left, right, right_name):
    for i in left:
        for j in right:
            if i['date'] == j['date']:
                merge_seasons(i['seasons'], j['seasons'], right_name)

def get_last_week():  
    # get bilibili below
    bangumi_list = get_target_week('bilibili')
    result={"result":bangumi_list}
    print('bilibili result')
    print(result)
    # get acfun below
    bangumi_list = get_target_week('acfun')
    # insert acfun into bilibili
    merge_list(result['result'], bangumi_list, 'acfun')
    print('acfun result')
    print(bangumi_list)

    # insert AGE into bilibili
    bangumi_list = get_target_week('AGE')
    merge_list(result['result'], bangumi_list, 'AGE')
    print('AGE result')
    print(bangumi_list)

    print('final result')
    print(result)
    return result

if __name__=='__main__':
    # data = get_last_week()
    data = get_detail_info()
    print(data)
