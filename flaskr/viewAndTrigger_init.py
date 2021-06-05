# 视图、函数、触发器的初始化模块


import pymysql
import traceback

# 作者：杨智麟
# 该视图为用户的番剧的详情信息查询提供便利
# 提供番剧的id,名称，制作公司，头图的信息
def create_view_detail_info(db):
    cursor=db.cursor()
    sql1="""
        drop view if exists detail_info;
        """
    sql2 = """
        CREATE view detail_info as (
        select bangumi_id, name,company_name,conduct_name,img
        from (((bangumi_list natural join bangumi_company) natural join bangumi_conduct)
 		natural join company) natural join conduct
        )
        """
    try:
        print('start to execute:')
        print(sql2)
        cursor.execute(sql1)
        cursor.execute(sql2)
        print('create success !')
    except:
        print('create error!')
        traceback.print_exc()
    cursor.close()



# 触发器
# 作者：陈家豪
# 触发器作用为：delete_on_bili: 在bilibili分表上删除某条bangumi信息后，检查其他分表上有无该bangumi信息
#                若其他分表上也没有，则在总表bangumi_list上删除这条bangumi信息。
#                delete_on_acfun的作用同上。
# 由于pymysql语法兼容问题，不能通过python执行下列函数创建该触发器，需要通过dbinit.sql脚本创建
def create_trigger_bangumi(db):
    cursor = db.cursor()
    #delete_on_bili
    sql1="""
        delimiter //
        drop trigger if exists delete_on_bili//
        create trigger delete_on_bili
        after delete on bilibili
        for each row
        begin
            if (ifexist_acfun(old.bangumi_id)=-1 AND ifexist_AGE(old.bangumi_id)=-1) then
                begin
                    delete from bangumi_list
                    where bangumi_list.bangumi_id = old.bangumi_id;
                end;
            end if;
        end; //
        delimiter ;
    """
    #delete_on_acfun
    sql2="""
        delimiter //
        drop trigger if exists delete_on_acfun//
        create trigger delete_on_acfun
        after delete on acfun
        for each row
        begin
            if (ifexist_bili(old.bangumi_id)=-1 AND ifexist_AGE(old.bangumi_id)=-1) then
                begin
                    delete from bangumi_list
                    where bangumi_list.bangumi_id = old.bangumi_id;
                end;
            end if;
        end; //
        delimiter ;
    """
    #delete_on_AGE
    sql3="""
        delimiter //
        drop trigger if exists delete_on_AGE//
        create trigger delete_on_AGE
        after delete on AGE
        for each row
        begin
            if (ifexist_bili(old.bangumi_id)=-1 AND ifexist_acfun(old.bangumi_id)=-1) then
                begin
                    delete from bangumi_list
                    where bangumi_list.bangumi_id = old.bangumi_id;
                end;
            end if;
        end; //
        delimiter ;
    """
    try:
        print('start to execute:')
        print(sql1)
        cursor.execute(sql1)
        print('create success !')
    except:
        print('create error!')
        traceback.print_exc()
    try:
        print(sql2)
        cursor.execute(sql2)
        print('create success !')
    except:
        print('create error!')
        traceback.print_exc()
    try:
        print(sql3)
        cursor.execute(sql3)
        print('create success !')
    except:
        print('create error!')
        traceback.print_exc()



# 函数
# 作者：陈家豪
# 函数作用：ifexist_bili函数作用为，输入bangumi的id，检测其是否在bilibili分表中
#           若存在，则返回id；若不存在，则返回-1.
#           函数ifexist_acfun的作用同上
# 由于pymysql语法兼容问题，不可通过以下python函数创建mysql函数，在dbinit.sql脚本中创建

def create_func_ifexist(db):
    cursor = db.cursor()
    sql1="""
        delimiter $$
        drop function if exists ifexist_bili$$
        create function ifexist_bili (id int) 
        returns int
        begin
            if (id in (select bangumi_id from bilibili)) then
                return(id);
            end if;
            return(-1);
        end$$
        delimiter ;
    """   
    sql2="""
        delimiter $$
        drop function if exists ifexist_acfun$$
        create function ifexist_acfun (id int) 
        returns int
        begin
            if (id in (select bangumi_id from acfun)) then
                return(id);
            end if;
            return(-1);
        end$$
        delimiter ;
    """ 
    sql3="""
        delimiter $$
        drop function if exists ifexist_AGE$$
        create function ifexist_AGE (id int) 
        returns int
        begin
            if (id in (select bangumi_id from AGE)) then
                return(id);
            end if;
            return(-1);
        end$$
        delimiter ;
    """ 
    try:
        print('start to execute:')
        print(sql1)
        cursor.execute(sql1)
        print('create success !')
        print(sql2)
        cursor.execute(sql2)
        print('create success !')
        print(sql3)
        cursor.execute(sql3)
        print('create success !')
    except:
        print('create error!')
        traceback.print_exc()


    

if __name__ == '__main__':
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    create_view_detail_info(db) #create view
    # create_func_ifexist(db)
    # create_trigger_bangumi(db)  #create tigger， 需要手动创建

    db.close()
    