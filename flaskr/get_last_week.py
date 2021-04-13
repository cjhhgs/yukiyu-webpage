import pymysql
import datetime

def get_list_of_date(day = '2021-04-07', target_table = 'bilibili'):
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
            



def get_last_week():
    today = datetime.date.today()
    # get bilibili below
    bangumi_list = list()
    for i in range(0,7):
        last_day = today + datetime.timedelta(days= -i)
        weekday = last_day.weekday()
        date = last_day.strftime("%Y-%m-%d")
        list_of_day = get_list_of_date(last_day)
        # solve mysql return void tuble when it is null
        if type(list_of_day) == type(()):
            list_of_day = []
        # update the play_url, make it become a dict
        for i in list_of_day:
            i['play_url'] = {'bilibili': i['play_url']}
        temp = {"date":date,"weekday":weekday,"seasons":list_of_day}
        bangumi_list.append(temp)
    new_list = sorted(bangumi_list, key=lambda keys: keys["weekday"])
    result={"result":new_list}
    print('bilibili result')
    print(result)
    # get acfun below
    bangumi_list = list()
    for i in range(0,7):
        last_day = today + datetime.timedelta(days= -i)
        weekday = last_day.weekday()
        date = last_day.strftime("%Y-%m-%d")
        list_of_day = get_list_of_date(last_day, 'acfun')
        # update the play_url, make it become a dict
        for i in list_of_day:
            i['play_url'] = {'acfun': i['play_url']}
        temp = {"date":date,"weekday":weekday,"seasons":list_of_day}
        bangumi_list.append(temp)
    new_list = sorted(bangumi_list, key=lambda keys: keys["weekday"])
    for i in result['result']:
        for j in new_list:
            if i['date']==j['date']:
                # print('merge left:')
                # print(i['seasons'])
                # print('merge right')
                # print(j['seasons'])
                merge_seasons(i['seasons'], j['seasons'], 'acfun')
    print('acfun result')
    print(new_list)

    print('final result')
    print(result)
    return result

if __name__=='__main__':
    data = get_last_week()
    # print(data)
