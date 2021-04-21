import pymysql
import traceback

def create_bangumi_table(db, table_name):
    cursor=db.cursor()
    sql = "CREATE TABLE %s(\
            bangumi_id int not NULL,\
            title varchar(50) not NULL,\
            play_url varchar(50) not NULL,\
            episode varchar(50) not NULL,\
            last_update date not NULL,\
            PRIMARY KEY (bangumi_id),\
            foreign key (bangumi_id) references bangumi_list(bangumi_id)\
            on update cascade\
            on delete cascade)ENGINE=InnoDB DEFAULT CHARSET=utf8;"% \
            (table_name)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('create success !')
    except:
        print('create table %s error!'%(table_name))
        traceback.print_exc()

if __name__ == '__main__':
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    create_bangumi_table(db,'AGE')
    db.close()