import traceback
import pymysql

db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')

# TODO: improve the robustness
def checkValibleTableName(targetTable):
    return targetTable != None

# this function call updataItem, insertItem, deleteItem
# according to the oldInfo and newInfo
# if oldInfo is None, call insert
# if newInfo is None, call delete
# else, call updata
def commitChangeToDatabase(oldInfo, newInfo, targetTable):
    if oldInfo == None and newInfo == None or not checkValibleTableName(targetTable):
        print('error ! invalid change!')
        print('oldInfo:', oldInfo)
        print('newInfo:', newInfo)
        print('targetTable:', targetTable)
        return -1
    returnStatus = 0
    if oldInfo == None:
        returnStatus = insertItem(oldInfo, newInfo, targetTable)
    elif newInfo == None:
        returnStatus = deleteItem(oldInfo, newInfo, targetTable)
    else:
        returnStatus = updateItem(oldInfo, newInfo, targetTable)
    return returnStatus

# shuffle : ((a,),(b,),(c,)) --> (a, b, c)
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
    
# get all tables, including table names and data
def getDatabase(target):
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
def getKeyValueString(name, data, seperate=','):
    res = ''
    for i in range(name.length):
        if isinstance(data[i], str):
            res += (name[i] + '=' + "'" + data[i] + "'")
        else:
            res += (name[i] + '=' + data[i])
        if i != name.length - 1:
            res += seperate
    return res

# return the string: value1 seperate value2...
# if strlization is True, when the data[i] is str, the value will be: 'value'
def getValueString(data, seperate=',', strlization = False):
    res = ''
    strlize = ''
    if strlization == True:
        strlize = "'"
    for i in range(data):
        if isinstance(data[i], str):
            res += (strlize + data[i] + strlize)
        else:
            res += data[i]
        if i != data.length - 1:
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
    valueStr = getValueString(newInfo, strlization=True)
    cursor = db.cursor()
    sql = """
            insert into %s
            %s
            values
            %s
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
    whereField = getKeyValueString(tableHead, oldInfo)
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
        
        