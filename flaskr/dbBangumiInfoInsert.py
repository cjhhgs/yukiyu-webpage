import traceback
import pymysql
from pymysql.cursors import Cursor
from db_bangumi_insert import nameComp
from moegirl import getProduceInfo

def getBangumiList(db):
    cursor = db.cursor()
    sql = 'select bangumi_id, name\
           from bangumi_list'
    try:
        cursor.execute(sql)
        bangumiList = cursor.fetchall()
        return bangumiList
    except:
        print('select from bangumi_list error !')
        traceback.print_exc()
    return ()

# to judge whether the bangumi is included bangumiInfoList
def isIncluded(bangumiName, bangumiInfoList):
    for i, item in enumerate(bangumiInfoList):
        if nameComp(bangumiName, item['name']):
            return i
    return -1

def insertConduct(bangumiItem, conduct, db):
    cursor = db.cursor()
    sql = 'insertIntoConduct(%d, %s, %s)'% \
            (*bangumiItem, conduct)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('execute success!')
    except:
        traceback.print_exc()

def insertCompany(bangumiItem, company, db):
    cursor = db.cursor()
    sql = 'insertIntoConduct(%d, %s, %s)'% \
            (*bangumiItem, company)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('execute success!')
    except:
        traceback.print_exc()


def insertInfo(bangumiInfoList, db):
    bangumiList = getBangumiList(db)
    # print(bangumiList)
    for item in bangumiList:
        index = isIncluded(item[1], bangumiInfoList)
        if index != -1:
            insertConduct()




if __name__ == '__main__':
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    bangumiInfoList = getProduceInfo()
    insertInfo(bangumiInfoList, db)