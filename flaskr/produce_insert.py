# 番剧的详细信息存储模块
# 获取moegirl爬虫爬取的数据，存储到数据库中

import moegirl
import pymysql
import merge_info
import db_bangumi_insert as DBI

def merge_produce_info(db):
    cursor=db.cursor()
    try:
        print('try to get produce info\n')
        produce_list=moegirl.getProduceInfo()
        print('get info successful')
    except:
        print('get info faild')

    for i in produce_list: 
        print('check ',i)
        id = DBI.if_exist(db,i["name"])
        print('id:',id)
        if id!=0:
            sql="call insertIntoCompany( %d,'%s','%s')\
                ;"%\
            (id,i['name'],i['production'])#如果是库中收录的番，则调用存储过程
            try:
                print('start to execute:')
                print(sql)
                cursor.execute(sql)
                print('insert success !')
            except:
                print('insert error!')
                traceback.print_exc()

            sql="call insertIntoConduct( %d,'%s','%s')\
                ;"%\
            (id,i['name'],i['conduct'])#如果是库中收录的番，则调用存储过程
            try:
                print('start to execute:')
                print(sql)
                cursor.execute(sql)
                print('insert success !')
            except:
                print('insert error!')
                traceback.print_exc()
        else:
            print("miss")

if __name__=='__main__':
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    merge_produce_info(db)


