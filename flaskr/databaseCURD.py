import pymysql

db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')

def signColumnsShuffle(input):
    res = []
    for i in input:
        res.append(i[0])
    return res

def getTableHead(tableName):
    print('start to get table head from ' + tableName)
    cursor = db.cursor()
    sql = "select column_name from information_schema.columns as col where col.table_name='%s'"%tableName
    cursor.execute(sql)
    res = cursor.fetchall()
    res = signColumnsShuffle(res)
    print('success ! \nget result: ')
    print(res)
    cursor.close()
    return res

def getTableData(tableName):
    cursor = db.cursor()
    print('start to get table data from ' + tableName)
    sql = "select * from %s"%tableName
    # print('start to execute:')
    # print(sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    print(res)
    cursor.close()
    return res

def getTableNames():
    # cursor = db.cursor()
    # print('start to get table names from yukiyu')
    # sql = "select table_name from information_schema.tables as tb where tb.table_schema = 'yukiyu'"
    # cursor.execute(sql)
    # res = cursor.fetchall()
    # # print('fetch res :')
    # # print(res)
    # res = signColumnsShuffle(res)
    # print('success ! \nget result: ')
    # print(res)
    # cursor.close()
    res = ['bangumi_list', 'bilibili', 'acfun', 'AGE', 'company', 'conduct', 'bangumi_conduct', 'bangumi_company', 'bangumi_cast']
    return res
    

def getTables(target):
    print('get url args:')
    print(target)
    res = {}
    for key in target:
        if target[key] != 'tables':
            # 获取数据表中的表头
            res[target[key]+'Header'] = getTableHead(target[key])
            # 获取数据表中的所有数据
            res[target[key]] = getTableData(target[key])
        else:
            # 获取数据库中的所有数据表名
            res['tableList'] = getTableNames()
    return res
