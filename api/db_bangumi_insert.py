import pymysql
import merge_info

def insert_new(db, bangumi_list):
    cursor=db.cursor()
    for item in bangumi_list:
        sql = "INSERT INTO bangumi_list\
            (name,img)\
            VALUES('%s','%s')"% \
            (item['name'],item['img'])
        print('try to insert:' ,sql)
        try:
            print('start excute')
            cursor.execute(sql)
            print('excute succeed')
            print('start commit')
            db.commit()
            print('succeed')
        except:
            db.rollback()
            print('error')

if __name__ == '__main__':
    # db = pymysql.connect("localhost", "zlyang", "123456", "yukiyu", charset='utf8')
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="zlyang", password="123456",charset='utf8')
    bangumi_list = merge_info.merge_info(True)
    print(bangumi_list)
    # bangumi_list = {'season':[{'name':'测试中文','img':'测试中文bbb.jpg'}]}
    insert_new(db,bangumi_list['season'])
    db.close()
            