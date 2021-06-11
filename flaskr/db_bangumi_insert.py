# 获取爬虫爬取的数据，格式化并插入到数据库中
# 该模块处理了总表-分表的依赖关系
# 即当有一个新番数据插入分表（如bilibili表）时，
# 在总表中检查是否存在该新番
# 若存在，则仅在bilibili中插入或更新，
# 若不存在，则在总表中也插入该番的条目

import pymysql
import time
import merge_info
import difflib
import traceback

# TODO: packing follow code to a class

# replace the common str to avoid confusing the nameComp function
def replaceSuffix(left, right):
    replaceTarget = [' ', '中配']
    for i in replaceTarget:
        left = left.replace(i, '$')
        right = right.replace(i, '%')
    return left, right

# bangumi name compare function
def nameComp(left, right):
    res = False
    left, right = replaceSuffix(left, right)
    if difflib.SequenceMatcher(None, left, right).quick_ratio() > 0.75:
        res = True
    else:
        matchPos = difflib.SequenceMatcher(None, left, right).get_matching_blocks()
        for it in matchPos:
            if it.size > 3:
                res = True
                # print('same block: "%s"' %(left[it.a:it.a+it.size]))
                break
    return res
        
# check whether a bangumi is in bangumi_list
# if exist, return the id of it
# if not, return 0
def if_exist(db,newName):
    # in our code, we split chinese name and English name by '-'
    # so we compare Chinese name and English name seperated
    cursor=db.cursor()
    # select all and check one by one
    sql = "select * from bangumi_list"
    try:
        cursor.execute(sql)
        res = cursor.fetchall()
        print('bangumi_list:', res)
        for i in res:
            curName = i[1]
            if nameComp(curName, newName):
                print('compare "%s" and "%s" is True\n\n\n'%(curName,newName))
                return i[0]         
        return 0
    except:
        print('not exist in bangumi_list')
        return 0

# use time to create the id
def create_id():
    ticks = int(time.time()*100)%10000000 
    return ticks

def insert_new(db, bangumi_dict):
    today = time.strftime("%Y-%m-%d", time.localtime())
    cursor=db.cursor()
    # key is the website info we use reptile got
    # for each website, we have diffrent table to store its info
    for key in bangumi_dict.keys():   
        # update each item in the web one by one    
        for item in bangumi_dict[key]:
            # check whether a bangumi is in database
            sql = "select bangumi_id from %s\
                    where title = '%s'"% \
                    (key,item['name'])
            try:
                print('start to select ! ', sql)
                cursor.execute(sql)
                print('start to fetch')
                result=cursor.fetchall()
                print('fetch result:' ,result)
                # if already exist, we just update the play_url and time
                if len(result) != 0:
                    sql = "UPDATE %s SET\
                    play_url =  '%s',  episode = '%s', last_update = '%s'\
                    where title = '%s' "% \
                    (key, item['play_url'], item['episode'], today, item['name'])   
                    print('try to update:' ,sql)
                    try:
                        print('start excute')
                        cursor.execute(sql)
                        print('excute success')
                        print('start commit')
                        db.commit()
                        print('success')
                    except:
                        db.rollback()
                        print('update error!')
                # if dosent exist we check whether it in 'bangumi_list' first
                else:
                    print('try to find in bangumi_list')
                    id = if_exist(db,item['name'])
                    print('id==%d'%id)
                    # if not in bangumi_list , this is a comletely new bangumi
                    # we create a new id and insert it into the bangumi_list first
                    if id == 0:
                        id = create_id()
                        # for completely new bangumi, we need to get its img first
                        # TODO: optimize this to just get the pic of the target and ignore the rest
                        new_dict = merge_info.merge_info(True)
                        print('start insert to bangumi list!')
                        img_url=None
                        for i in new_dict[key]:
                            if i['name'] == item['name']:
                                img_url = i['img']
                                break
                        sql = "insert into bangumi_list\
                            (bangumi_id, name, img)\
                            VALUES(%d, '%s', '%s')"% \
                            (id, item['name'], img_url)
                        print('insert item:',sql)
                        try:
                            cursor.execute(sql)
                            db.commit()
                            print('success')
                        except:
                            print('insert into bangumi_list error!')
                            db.rollback()
                            traceback.print_exc()
                    # we insert this bangumi to current web's table
                    sql = "insert into %s\
                            (bangumi_id, title, play_url, episode, last_update)\
                            VALUES(%d, '%s', '%s','%s', '%s')"% \
                            (key, id, item['name'], item['play_url'], item['episode'], today)
                    try:
                        print('start insert to %s' %key)
                        print('insert item: ' ,sql)
                        cursor.execute(sql)
                        db.commit()
                        print('success')
                    except:
                        db.rollback()
                        print('insert into %s error!' %key)
                        traceback.print_exc()
            except:
                print('query error!')
                traceback.print_exc()
                      

def insert_bangumi(db):
    print('start to get bangumi')
    bangumi_dict = merge_info.merge_info(False)
    print(bangumi_dict)
    # bangumi_dict = {'season':[{'name':'测试中文','img':'测试中文bbb.jpg'}]}
    insert_new(db,bangumi_dict) 


if __name__ == '__main__':
    # db = pymysql.connect("localhost", "zlyang", "123456", "yukiyu", charset='utf8')
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    print('start to get bangumi')
    bangumi_dict = merge_info.merge_info(False)
    print(bangumi_dict)
    # bangumi_dict = {'season':[{'name':'测试中文','img':'测试中文bbb.jpg'}]}
    insert_new(db,bangumi_dict)
    db.close()
            