import pymysql

if __name__=='__main__':
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    cursor = db.cursor()
    sql="""
        drop procedure if exists test;
        create procedure test(in p1 int)
        begin
        end;
    """
    sql1="drop procedure if exists test;"
    sql2="""create procedure test(in p1 int)
        begin
        end;"""
    sql3="delimiter /"
    cursor.execute(sql3)
    db.close()