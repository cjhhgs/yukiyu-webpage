import pymysql
import traceback
from werkzeug.security import check_password_hash, generate_password_hash
from itertools import chain


#默认创建普通用户，授权select
def createUser(name,password):
    db = pymysql.connect(host="localhost", port=3306, db="mysql", user="root", password="123456",charset='utf8')
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
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="root", password="123456",charset='utf8')
    cursor=db.cursor()
    data = privilegeOfUser(name)
    priv = data['privilege']
    sql2 = """
    insert into user(name,password,privilege) 
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
    db = pymysql.connect(host="localhost", port=3306, db="mysql", user="root", password="123456",charset='utf8')
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
    delete from yukiyu.user
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


#授权为超级用户，实现所有权限
def grantSuperUser(name):
    host='%'
    db = pymysql.connect(host="localhost", port=3306, db="mysql",user="root", password="123456", charset="utf8")
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
        traceback.print_exc()

    data = privilegeOfUser(name)
    priv = data['privilege']
    sql2 = """
    update yukiyu.user
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

#授权为普通用户，select权限
def grantOrdinartUser(name):
    host = '%'
    db = pymysql.connect(host="localhost", port=3306, db="mysql",user="root", password="123456", charset="utf8")
    cursor = db.cursor()
    sql1="revoke all privileges on yukiyu.* from '%s'@'%s';"%\
    (name,host)
    sql2="""grant select on yukiyu.* to '%s'@'%s';
    """%\
    (name,host)
    try:
        print('start to execute:')
        print(sql1)
        cursor.execute(sql1)
        print('revoke success !')
    except:
        print('revoke error!')
        traceback.print_exc()

    try:
        print('start to execute:')
        print(sql2)
        cursor.execute(sql2)
        print('grant success !')
    except:
        print('grant error!')
        traceback.print_exc()

    data = privilegeOfUser(name)
    priv = data['privilege']
    sql3 = """
    update yukiyu.user
    set privilege = '%s'
    where name = '%s';
    """%\
    (priv,name)
    try:
        print('start to execute:')
        print(sql3)
        cursor.execute(sql3)
        print('update success !')
    except:
        print('update error!')
        traceback.print_exc()
    
    cursor.close()
    db.close()

#为指定用户增加指定权限
def addPrivForUser(name,privilege):
    host='%'
    db = pymysql.connect(host="localhost", port=3306, db="mysql",user="root", password="123456", charset="utf8")
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
    update yukiyu.user
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

#删除指定用户的某权限
def delPrivForUser(name,privilege):
    host='%'
    db = pymysql.connect(host="localhost", port=3306, db="mysql",user="root", password="123456", charset="utf8")
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
    update yukiyu.user
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
    db = pymysql.connect(host="localhost", port=3306, db="mysql",user="root", password="123456", charset="utf8")
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
    db = pymysql.connect(host="localhost", port=3306, db="mysql",user="root", password="123456", charset="utf8")
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
    db = pymysql.connect(host="localhost", port=3306, db="mysql",user="root", password="123456", charset="utf8")
    cursor=db.cursor(pymysql.cursors.DictCursor)
    sql = "select if_manager, user_id, name, privilege  from yukiyu.user;"
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
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu",user="root", password="123456", charset="utf8")
    cursor=db.cursor(pymysql.cursors.DictCursor)
    sql = "select password from yukiyu.user where name = '%s'"%\
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

if __name__ == '__main__':
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="root", password="123456",charset='utf8')
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