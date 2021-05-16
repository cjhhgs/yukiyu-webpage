import traceback
import pymysql

# db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
global db

# TODO: improve the robustness
def checkValibleTableName(targetTable):
    return targetTable != None

# this function call updataItem, insertItem, deleteItem
# according to the oldInfo and newInfo
# if oldInfo is None, call insert
# if newInfo is None, call delete
# else, call updata
def commitChangeToDatabase(oldInfo, newInfo, targetTable):
    global db
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    if oldInfo == None and newInfo == None or not checkValibleTableName(targetTable):
        print('error ! invalid change!')
        print('oldInfo:', oldInfo)
        print('newInfo:', newInfo)
        print('targetTable:', targetTable)
        return -1
    returnStatus = 0
    if oldInfo == None:
        returnStatus = insertItem(newInfo, targetTable)
    elif newInfo == None:
        returnStatus = deleteItem(oldInfo, targetTable)
    else:
        returnStatus = updateItem(oldInfo, newInfo, targetTable)
    return returnStatus

# shuffle : ((a,),(b,),(c,)) --> (a, b, c)
def signColumnsShuffle(input):
    res = []
    for i in input:
        res.append(i[0])
    return res

# shuffle datetime.date to str: 2021-02-20
def datetimeShffle(input):
    res = []
    for i in input:
        temp = []
        for k in i:
            temp.append(str(k))
        res.append(temp)
    return res

def getTableHead(tableName):
    print('start to get table head from ' + tableName)
    cursor = db.cursor()
    sql = "select column_name from information_schema.columns as col where col.table_name='%s'"%tableName
    print('start to execute:')
    print(sql)
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
    res = datetimeShffle(res)
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
    
# get all tables, including table names and data
def getDatabase(target):
    global db
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
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

# return the string: key1=value1 seperate key2=valuue2...
# def getKeyValueString(name, data, seperate=','):
#     res = ''
#     length = len(name)
#     for i in range(length):
#         if isinstance(data[i], str):
#             res += (name[i] + '=' + "'" + data[i] + "'")
#         else:
#             res += (name[i] + '=' + data[i])
#         if i != length - 1:
#             res += seperate
#     return res

# return the string: key1=value1 seperate key2=valuue2...
def getKeyValueString(name, data, seperate=','):
    res = ''
    seperate = ' ' + seperate + ' '
    length = len(name)
    for i in range(length):
        res += (name[i] + '=' + "'" + str(data[i]) + "'")
        if i != length - 1:
            res += seperate
    return res

# # return the string: value1 seperate value2...
# # if strlization is True, when the data[i] is str, the value will be: 'value'
# def getValueString(data, seperate=',', strlization = False):
#     res = ''
#     strlize = ''
#     if strlization == True:
#         strlize = "'"
#     length = len(data)
#     for i in range(length):
#         if isinstance(data[i], str):
#             res += (strlize + data[i] + strlize)
#         else:
#             res += data[i]
#         if i != length - 1:
#             res += seperate
#     return res

# # return the string: value1 seperate value2...
# # if strlization is True, when the data[i] is str, the value will be: 'value'
def getValueString(data, seperate=',', strlization = False):
    seperate = ' ' + seperate + ' '
    res = ''
    strlize = ''
    if strlization == True:
        strlize = "'"
    length = len(data)
    for i in range(length):
        res += (strlize + str(data[i]) + strlize)
        if i != length - 1:
            res += seperate
    return res

def updateItem(oldInfo, newInfo, targetTable):
    tableHead = getTableHead(targetTable)
    setField = getKeyValueString(tableHead, newInfo, ',')
    whereField = getKeyValueString(tableHead, oldInfo, 'and')
    cursor = db.cursor()
    returnStatus = 0
    sql = """
            update %s
            set %s
            where %s
          """%(targetTable, setField, whereField)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        db.commit()
        print('success !')
        returnStatus = 1
    except:
        print('updata error !')
        db.rollback()
        traceback.print_exception()
        returnStatus = 0
    db.close()
    return returnStatus

def insertItem(newInfo, targetTable):
    tableHeadStr = getValueString(getTableHead(targetTable))
    valueStr = getValueString(newInfo,strlization=True)
    cursor = db.cursor()
    sql = """
            insert into %s
            (%s)
            values
            (%s)
        """%(targetTable, tableHeadStr, valueStr)
    returnStatus = 0
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        db.commit()
        print('success !')
        returnStatus = 1
    except:
        print('insert error !')
        db.rollback()
        traceback.print_exc()
        returnStatus = 0
    db.close()
    return returnStatus

def deleteItem(oldInfo, targetTable):
    tableHead = getTableHead(targetTable)
    whereField = getKeyValueString(tableHead, oldInfo, 'and')
    cursor = db.cursor()
    sql = """
            delete from %s
            where %s
        """%(targetTable, whereField)
    returnStatus = 0
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        db.commit()
        print('success !')
        returnStatus = 1
    except:
        print('delete error !')
        db.rollback()
        traceback.print_exc()
        returnStatus = 0
    db.close()
    return returnStatus
        
        