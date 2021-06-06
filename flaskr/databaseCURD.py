# 该模块提供了一个数据库的通用CURD接口
# 通过该接口能够快速进行数据库的增删查改功能
# 该模块还提供了获取数据库所有表表名，各表表头的接口

import traceback
import pymysql
from userManage import commmitChangeToUserlist, privilegeOfUser, ifManage


global db

# TODO: improve the robustness
def checkValibleTableName(targetTable, user):
    if user != None and targetTable == 'user_list':
        return user in getSuperUser()
    return targetTable != None

def commitChangeToDatabase(oldInfo, newInfo, targetTable, user = None):
    returnStatu = changeProcess(oldInfo, newInfo, targetTable, user)
    if returnStatu == 0:
        info = '错误的数据格式！'
    elif returnStatu == -1:
        info = '该表不存在！'
    elif returnStatu == -2:
        info = '非法访问：未经过用户认证'
    elif returnStatu == -3:
        info = '非法访问：用户无该权限'
    elif returnStatu == -4:
        info = '错误的数据格式：管理员用户拥有增删查改所有权限'
    elif returnStatu == -5:
        info = '用户名重复'
    elif returnStatu == 1:
        info = '运行成功！'
    else:
        info = '未知错误！'
    return {'statu': returnStatu, 'info': info}

# this function call updataItem, insertItem, deleteItem
# according to the oldInfo and newInfo
# if oldInfo is None, call insert
# if newInfo is None, call delete
# else, call updata
#
# OK code: return 1
# error code:
# 0  : sql run time error
# -1 : invalid target table
# -2 : user is None
# -3 : user has not target privilege
# -4 : manager's privilege is not 'YYYY' 
# -5 : user name chongfu
def changeProcess(oldInfo, newInfo, targetTable, user = None):
    if user == None:
        return -2
    userPrivilege = privilegeOfUser(user).get('privilege')

    global db
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    if oldInfo == None and newInfo == None or not checkValibleTableName(targetTable, user):
        print('error ! invalid change!')
        print('oldInfo:', oldInfo)
        print('newInfo:', newInfo)
        print('targetTable:', targetTable)
        return -1
    returnStatus = 0
    if targetTable == 'user_list':
        if ifManage(user) == 'Y':
            return commmitChangeToUserlist(oldInfo, newInfo)
        else:
            return -3

    if oldInfo == None:
        if userPrivilege[1] == 'Y':
            returnStatus = insertItem(newInfo, targetTable)
        else:
            returnStatus = -3
    elif newInfo == None:
        if userPrivilege[3] == 'Y':
            returnStatus = deleteItem(oldInfo, targetTable)
        else:
            returnStatus = -3
    else:
        if userPrivilege[1] == 'Y':
            returnStatus = updateItem(oldInfo, newInfo, targetTable)
        else:
            returnStatus = -3
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

def getSuperUser():
    cursor = db.cursor()
    sql = "select name from user_list where if_manager = 'Y'"
    print('start to execute:')
    print(sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    res = signColumnsShuffle(res)
    print('execute success!')
    print('result:' ,res)
    cursor.close()
    return res

def getTableNames(user):
    cursor = db.cursor()
    print('start to get table names from yukiyu')
    sql = "select table_name from information_schema.tables as tb where tb.table_schema = 'yukiyu'"
    cursor.execute(sql)
    res = cursor.fetchall()
    res = signColumnsShuffle(res)
    print('success ! \nget result: ')
    print(res)
    cursor.close()
    # 非超级用户不允许查看user列表
    if user not in getSuperUser():
        res.remove('user_list')
    # 将主表放在最前面
    res.remove('bangumi_list')
    res.insert(0, 'bangumi_list')
    return res
    
# get all tables, including table names and data
def getDatabase(target, user):
    global db
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    print('get url args:')
    print(target)
    res = {}
    selectPriv = privilegeOfUser(user).get('privilege')[0]
    for key in target:
        if target[key] != 'tables':
            # 获取数据表中的表头
            res[target[key]+'Header'] = getTableHead(target[key])
            # 获取数据表中的所有数据
            if selectPriv == 'Y':
                res[target[key]] = getTableData(target[key])
            else:
                res[target[key]] = None
        else:
            # 获取数据库中的所有数据表名
            res['tableList'] = getTableNames(user)
    return res


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



# return the string: value1 seperate value2...
# if strlization is True, when the data[i] is str, the value will be: 'value'
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
        
def getUserList():
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    cursor = db.cursor()
    sql = 'select name, password, user_id from user_list'
    cursor.execute(sql)
    res = cursor.fetchall()
    return res        