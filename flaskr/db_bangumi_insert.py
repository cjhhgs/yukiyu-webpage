import pymysql
import time
import merge_info
import difflib
import traceback

# TODO: packing follow code to a class

# check whether a bangumi is in bangumi_list
# if exist, return the id of it
# if not, return 0
def if_exist(db,name):
    cursor=db.cursor()
    # select all and check one by one
    sql = "select * from bangumi_list"
    try:
        cursor.execute(sql)
        res = cursor.fetchall()
        print('bangumi_list:', res)
        for i in res:
            name = i[1].split('-')
            for item in name:
                # we use the string diff to approximate matching
                # optimize the matching rule here if needed
                if difflib.SequenceMatcher(None, name, item).quick_ratio() > 0.75:
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
                        print('excute succeed')
                        print('start commit')
                        db.commit()
                        print('succeed')
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
                            print('succeed')
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
                        print('succeed')
                    except:
                        db.rollback()
                        print('insert into %s error!' %key)
            except:
                print('query error!')
                traceback.print_exc()
                      
                
           


if __name__ == '__main__':
    # db = pymysql.connect("localhost", "zlyang", "123456", "yukiyu", charset='utf8')
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    bangumi_dict = merge_info.merge_info(False)
    print(bangumi_dict)
    # bangumi_dict = {'season':[{'name':'测试中文','img':'测试中文bbb.jpg'}]}
    insert_new(db,bangumi_dict)
    db.close()
            