import pymysql

db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="zlyang", password="123456",charset='utf8')
cursor = db.cursor()
name_list=['aaa','bbb']
for i in name_list:
    sql = "select name from bangumi_list\
            where name = '%s'"%\
            i
    try:
        cursor.execute(sql)
        res=cursor.fetchall()
        if len(res) == 0:
            print('void!')
        else:
            print(res)
    except:
        print('select error!')