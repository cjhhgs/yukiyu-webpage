# select distinct name, company_name, conduct_name, img
# from (((bangumi_list natural join bangumi_company) natural join bangumi_conduct)
# 		natural join company) natural join conduct;

import pymysql
import traceback

def create_view_detail_info(db):
    cursor=db.cursor()
    sql1="""
        drop view if exists detail_info;
        """
    sql2 = """
        CREATE view detail_info as (
        select name,company_name,conduct_name,img
        from (((bangumi_list natural join bangumi_company) natural join bangumi_conduct)
 		natural join company) natural join conduct;
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

def create_trigger_1(db):
    cursor = db.cursor()
    
    

if __name__ == '__main__':
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    #initProduceTbale(db)
    # createStoreProcedureBConduct(db)
    # createStoreProcedureBCompany(db)
    db.close()
    