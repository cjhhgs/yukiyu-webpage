import pymysql
import traceback
from werkzeug.security import check_password_hash, generate_password_hash
from itertools import chain


#默认创建普通用户，授权select
def createUser(name,password):
    db = pymysql.connect(host="localhost", port=3306, db="mysql", user="jhchen", password="123456",charset='utf8')
    cursor = db.cursor()
    host = '%'
    sql1 = "create user '%s'@'%s' identified by '%s';"%\
        (name,host,password)
    sql11="grant select on yukiyu.* to '%s'@'%s';"%\
    (name, host)
   
    cursor.execute("select user from db")
    elems = cursor.fetchall()
    res = list(chain.from_iterable(elems))
    print(res)
    if name in res:
        print("用户%s已存在"/(name))
        return

    try:
        print('start to execute:')
        print(sql1)
        print(sql11)
        cursor.execute(sql1)
        cursor.execute(sql11)
        print('create success !')
    except:
        print('create user error!')
        traceback.print_exc()
    db.close()


    #在yukiyu库中的user插入同样
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    cursor=db.cursor()
    data = privilegeOfUser(name)
    priv = data['privilege']
    sql2 = """
    insert into user_list(name,password,privilege) 
    values
    ('%s','%s','%s');"""%\
    (name,generate_password_hash(password),priv)
    try:
        print('start to execute:')
        print(sql2)
        cursor.execute(sql2)
        db.commit()
        print('insert success !')
    except:
        print('insert error!')
        traceback.print_exc()

    cursor.close()
    db.close()

#删除用户
def dropUser(name):
    db = pymysql.connect(host="localhost", port=3306, db="mysql", user="jhchen", password="123456",charset='utf8')
    cursor = db.cursor()
    host = '%'
    sql="drop user '%s'@'%s';"%\
    (name,host)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        db.commit()
        print('drop success !')
    except:
        print('drop user error!')
        traceback.print_exc()

    sql2 = """
    delete from yukiyu.user_list
    where name = '%s';
    """%\
    (name)
    try:
        print('start to execute:')
        print(sql2)
        cursor.execute(sql2)
        db.commit()
        print('delete user success !')
    except:
        print('delete user error!')
        traceback.print_exc()


    cursor.close()
    db.close()

    return 1


def ifManage(name):
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu",user="jhchen", password="123456", charset="utf8")
    sql = """
        select if_manager 
        from user
        where name = '%s';
    """%\
        (name)
    cursor=db.cursor(pymysql.cursors.DictCursor)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        print('success !')
    except:
        print('error!')
        traceback.print_exc()
    
    return data[0]['if_manager']


#授权为管理员用户，实现所有权限
def grantSuperUser(name):
    if ifManage(name)=='Y':
        print("success")
        return 1

    host='%'
    db = pymysql.connect(host="localhost", port=3306, db="mysql",user="jhchen", password="123456", charset="utf8")
    cursor = db.cursor()
    sql="""
    grant all privileges on yukiyu.* to '%s'@'%s';
    """%\
    (name,host)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('grant success !')
    except:
        print('grant error!')
        db.rollback()
        traceback.print_exc()
        return 0


    data = privilegeOfUser(name)
    priv = data['privilege']
    sql2 = """
    update yukiyu.user_list
    set privilege = '%s'
    where name = '%s';
    """%\
    (priv,name)
    try:
        print('start to execute:')
        print(sql2)
        cursor.execute(sql2)
        print('update success !')
    except:
        print('update error!')
        db.rollback()
        traceback.print_exc()
        return 0

    sql3 = """
        update yukiyu.user_list
        set if_manager = 'Y'
        where name = '%s';
    """%\
        (name)
    try:
        print('start to execute:')
        print(sql3)
        cursor.execute(sql3)
        print('update success !')
    except:
        print('update error!')
        db.rollback()
        traceback.print_exc()
        return 0


    cursor.close()
    db.close()
    return 1

#授权为普通用户，select权限
def grantOrdinartUser(name):

    if(ifManage(name)=='N'):
        print("success")
        return 1
    

    host = '%'
    db = pymysql.connect(host="localhost", port=3306, db="mysql",user="jhchen", password="123456", charset="utf8")
    cursor = db.cursor()
    sql1="revoke all privileges on yukiyu.* from '%s'@'%s';"%\
    (name,host)
    try:
        print('start to execute:')
        print(sql1)
        cursor.execute(sql1)
        print('revoke success !')
    except:
        print('revoke error!')
        db.rollback()
        traceback.print_exc()
        return 0

    changePrivilege(name, 'YYYY')
    
    cursor.close()
    db.close()


# 查看指定权限
def checkOnePriv(name, privilege):
    s = privilege+'_priv'
    db = pymysql.connect(host="localhost", port=3306, db="mysql",user="jhchen", password="123456", charset="utf8")
    cursor=db.cursor(pymysql.cursors.DictCursor)
    sql = """
        select %s_priv
        from db
        where Db = 'yukiyu' and User = '%s';
    """%\
    (name)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        print('success !')
    except:
        print('error!')
        traceback.print_exc()
    
    return data[0][s]


#为指定用户增加指定权限
def addPrivForUser(name,privilege):

    if checkOnePriv(name,privilege)=='Y':
        print("succsee")
        return 1


    host='%'
    db = pymysql.connect(host="localhost", port=3306, db="mysql",user="jhchen", password="123456", charset="utf8")
    cursor = db.cursor()
    sql1 = "grant %s on yukiyu.* to '%s'@'%s';"%\
        (privilege,name,host)
    try:
        print('start to execute:')
        print(sql1)
        cursor.execute(sql1)
        print('grant success !')
    except:
        print('grant error!')
        traceback.print_exc()

    data = privilegeOfUser(name)
    priv = data['privilege']
    sql2 = """
    update yukiyu.user_list
    set privilege = '%s'
    where name = '%s';
    """%\
    (priv,name)
    try:
        print('start to execute:')
        print(sql2)
        cursor.execute(sql2)
        print('update success !')
    except:
        print('update error!')
        traceback.print_exc()
    
    cursor.close()
    db.close()
    return 1

#删除指定用户的某权限
def delPrivForUser(name,privilege):

    if(checkOnePriv(name , privilege)=='N'):
        print("success")
        return 1

    host='%'
    db = pymysql.connect(host="localhost", port=3306, db="mysql",user="jhchen", password="123456", charset="utf8")
    cursor = db.cursor()
    sql1 = "revoke %s on yukiyu.* from '%s'@'%s';"%\
        (privilege,name,host)
    try:
        print('start to execute:')
        print(sql1)
        cursor.execute(sql1)
        print('grant success !')
    except:
        print('grant error!')
        traceback.print_exc()
    
    data = privilegeOfUser(name)
    priv = data['privilege']
    sql2 = """
    update yukiyu.user_list
    set privilege = '%s'
    where name = '%s';
    """%\
    (priv,name)
    try:
        print('start to execute:')
        print(sql2)
        cursor.execute(sql2)
        print('update success !')
    except:
        print('update error!')
        traceback.print_exc()

    cursor.close()
    db.close()


#查询指定用户权限
def privilegeOfUser(name):
    db = pymysql.connect(host="localhost", port=3306, db="mysql",user="jhchen", password="123456", charset="utf8")
    cursor=db.cursor(pymysql.cursors.DictCursor)
    sql = """
        select User, select_priv, insert_priv, update_priv, delete_priv, create_priv, drop_priv
        from db
        where Db = 'yukiyu' and User = '%s';
    """%\
    (name)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('success !')
    except:
        print('error!')
        traceback.print_exc()
    
    data = cursor.fetchall()

    a=data[0]["select_priv"]
    b=data[0]["insert_priv"]
    c=data[0]["update_priv"]
    d=data[0]["delete_priv"]

    s=a+b+c+d

    dict = {'name': data[0]['User'],'privilege':s}

    print(dict)
    return dict



#查看所有用户及权限
def privilegeOfAllUser():
    db = pymysql.connect(host="localhost", port=3306, db="mysql",user="jhchen", password="123456", charset="utf8")
    cursor=db.cursor(pymysql.cursors.DictCursor)

    sql = """
        select User, select_priv, insert_priv, update_priv, delete_priv, create_priv, drop_priv
        from db
        where Db = 'yukiyu';
    """
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('success !')
    except:
        print('error!')
        traceback.print_exc()

    data = cursor.fetchall()
    cursor.close()
    db.close()
    list = []
    for item in data:
        a=item['select_priv']
        b=item['insert_priv']
        c=item['update_priv']
        d=item['delete_priv']
        s=a+b+c+d
        list.append({'name': item['User'],'privilege':s})


    print(list)
    return list

def printAllUser():
    db = pymysql.connect(host="localhost", port=3306, db="mysql",user="jhchen", password="123456", charset="utf8")
    cursor=db.cursor(pymysql.cursors.DictCursor)
    sql = "select if_manager, user_id, name, privilege  from yukiyu.user_list;"
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('success !')
    except:
        print('error!')
        traceback.print_exc()
    data = cursor.fetchall()
    print(data)

#返回用户密码hash值
def getPassword(name):
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu",user="jhchen", password="123456", charset="utf8")
    cursor=db.cursor(pymysql.cursors.DictCursor)
    sql = "select password from yukiyu.user_list where name = '%s'"%\
        (name)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('success !')
    except:
        print('error!')
        traceback.print_exc()
    
    data = cursor.fetchall()
    password_hash = data[0]['password']
    
    print(password_hash)
    return password_hash


def changePrivilege(name,priv):
    
    if priv[0]=='Y':
        addPrivForUser(name,'select')
    else:
        delPrivForUser(name,'select')

    if priv[1]=='Y':
        addPrivForUser(name,'insert')
    else:
        delPrivForUser(name,'insert')
    
    if priv[2]=='Y':
        addPrivForUser(name,'delete')
    else:
        delPrivForUser(name,'delete')

    if priv[3]=='Y':
        addPrivForUser(name,'update')
    else:
        delPrivForUser(name,'update')
    
    return 1



#包装函数
def commmitChangeToUserlist(oldInfo, newInfo):
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    if oldInfo == None:
        returnStatus = insertItem(newInfo)
    elif oldInfo==None:
        returnStatus = deleteItem(oldInfo)
    else:
        returnStatus = updateItem(newInfo, oldInfo)
    
    return returnStatus


def insertItem(newInfo):
    status=1
    ifManage = newInfo[0]
    name = newInfo[1]
    password = newInfo[2]
    privilege = newInfo[3]
    createUser(name,password)
    changePrivilege(name,privilege)
    
    return status

def deleteItem(oldInfo):
    status=1
    name = oldInfo[1]
    dropUser(name)

    return status

def updateItem(newInfo, oldInfo):
    returnStatus = 1

    nifManage=newInfo[0]
    nname=newInfo[1]
    npassword=newInfo[2]
    npriv=newInfo[3]

    oifManage=oldInfo[0]
    oname=oldInfo[1]
    opassword=oldInfo[2]
    opriv=oldInfo[3]


    
    if(npriv != opriv):
        changePrivilege(oname,npriv)
    if(nifManage!=oifManage):
        changeIfManage(oname,nifManage)
    if(oname != nname):
        changeName(oname,nname)

    return returnStatus


#用户改姓名
def changeName(oname,nname):
    db = pymysql.connect(host="localhost", port=3306, db="mysql", user="jhchen", password="123456",charset='utf8')
    cursor=db.cursor()

    sql1 = """
    update user 
    set user='%s' 
    where user = '%s';"""%\
        (nname, oname)
    try:
        print('start to execute:')
        print(sql1)
        cursor.execute(sql1)
        db.commit()
        print('success !')
        returnStatus = 1
    except:
        print('updata user error !')
        db.rollback()
        traceback.print_exception()
        returnStatus = 0
        return returnStatus

    sql2="""
    update yukiyu.user_list 
    set name = '%s'
    where name = '%s';"""%\
        (nname,oname)
    try:
        print('start to execute:')
        print(sql2)
        cursor.execute(sql2)
        db.commit()
        print('success !')
        returnStatus = 1
    except:
        print('updata user error !')
        db.rollback()
        traceback.print_exception()
        returnStatus = 0
        return returnStatus

    return 1

def changeIfManage(name,nIfMnage):
    db = pymysql.connect(host="localhost", port=3306, db="mysql", user="jhchen", password="123456",charset='utf8')
    cursor=db.cursor()

    if(nIfMnage=='Y'):
        grantSuperUser(name)
    else:
        grantOrdinartUser(name)

    sql1 = """
    
    """
    try:
        print('start to execute:')
        print(sql1)
        cursor.execute(sql1)
        db.commit()
        print('success !')
        returnStatus = 1
    except:
        print('updata user error !')
        db.rollback()
        traceback.print_exception()
        returnStatus = 0
        return returnStatus



if __name__ == '__main__':
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    #dropUser('xxx')
    #createUser('xxx','123456')
    #grantSuperUser('cy')
    #grantOrdinartUser('cyy')
    #addPrivForUser('cyy','delete')
    #delPrivForUser('cyy','delete')
    #privilegeOfAllUser()
    #privilegeOfUser('cyy')
    
    printAllUser()
    getPassword('xxx')

    db.close()