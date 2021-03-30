import pymysql
import datetime
import time

def get_list_of_date(day):
    date = day.strftime("%Y-%m-%d")
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    cursor = db.cursor(pymysql.cursors.DictCursor)  #返回值为字典格式
    sql1 = """
        select  bangumi_id, name, img, bilibili.play_url,bilibili.episode
        from    bangumi_list natural join bilibili
        where bilibili.last_update = '%s'
        """% \
        (date)
    cursor.execute(sql1)
    data = cursor.fetchall()    #列表
    cursor.close()
    db.close()

    return data
    
def get_last_week():
    today = datetime.date.today()

    bangumi_list = list()
    for i in range(0,6):
        last_day = today + datetime.timedelta(days= -i)
        weekday = last_day.weekday()
        date = last_day.strftime("%Y-%m-%d")
        list_of_day = get_list_of_date(last_day)
        temp = {"date":date,"weekday":weekday,"seasons":list_of_day}
        bangumi_list.append(temp)
    new_list = sorted(bangumi_list, key=lambda keys: keys["weekday"])
    result={"result":new_list}
    print(result)
    return result

if __name__=='__main__':
    get_last_week()



