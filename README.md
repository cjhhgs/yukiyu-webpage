# 番剧更新表及番剧详情数据库

### 项目网站地址

http://106.15.77.207/yukiyu

## 项目背景

该项目立足于目前各大平台网站的番剧信息较为分散，用户需要辗转多个平台才能获取较为完整的番剧信息的背景下，实现了各大平台网站番剧信息的整合。将各大平台网站的番剧更新信息及番剧详情信息整合制表，展现在我们的网页上。

## 需求分析

### 番剧更新表

系统维护在播新番的当前更新集数，播放地址链接，宣传图，等内容。

番剧更新主要来源于`bilibili`，`ACfun`两个个网站。

所有信息均通过爬虫以及python脚本进行动态维护。

### 番剧详情表

针对每个番剧，提供该番剧的详情信息，包括制作公司，监督，声优等内容。

番剧详情主要来自于萌娘百科。

信息通过爬虫python脚本动态维护

### 用户管理

系统用户分为超级管理员用户和普通管理员用户。

#### 普通管理员

可查看数据库中的内容，可拥有删除、修改、添加番剧信息等权力。

#### 超级管理员

拥有数据库的完全控制权，包括查看所有用户资料，创建新用户，用户授权等操作。

## 数据库概念设计

![image-20210605085143470](README.assets/image-20210605085143470.png)

## 数据库结构

### 数据库各表简介

#### bangumi_list表

该表是本数据库的核心总表。

该表记录了本数据库的所有番剧目录信息，严格来讲其它表（除了用户表）都是为其提供修饰信息的。

#### bilibili表/acfun表

该表提供了番剧更新的详细信息。

该表提供番剧在对应网站的最新集数，播放地址，更新日期等数据。

#### company制作公司表

该表记录了各大制作公司。

该表提供制作公司的名称和代表作品（还可以添加制作公司的其他信息，由于数据来源较为困难等原因未在本项目中添加）。

#### conduct监督表

该表记录了监督的详细信息。

该表提供监督姓名和代表作品（还可以添加监督个人的其他信息，由于数据来源较为困难等原因未在本项目中添加）。

#### bangumi_cast声优表

该表记录各个番剧的声优。

该表提供番剧id——声优姓名关系，由于声优个人信息数据获取困难，本项目中并未将声优单独列表，而仅仅放于关系表中。

#### user_list用户表

该表记录用户的详细信息。

该表提供用户的用户名，密码（采用`werkzeug.security`中的`generate_password_hash`加密），用户权限等信息。

### 数据库各表间关系

`bangumi_list`表是本数据库的核心总表。

在`bangumi_list`表中的番剧，可在`bilibili`表和`acfun`表中有一条或多条详细信息。

在`bangumi_list`表中的番剧，可在`conduct`监督表中有监督对应。

在`bangumi_list`表中的番剧，可在`company`制作公司中有制作公司对应。

在`bangumi_list`表中的番剧，可在`bangumi_cast`声优表中有多位声优对应。

## 数据库实现

### 建表

```mysql
-- 创建banguni_list总表
create table if not exists bangumi_list(
    bangumi_id int not null,
    name varchar(80) not null,
    img varchar(100) not null,
    primary key (bangumi_id))ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建各视频网站分表
-- 创建bilibili分表
CREATE TABLE if not exists bilibili(
    bangumi_id int not NULL,
    title varchar(50) not NULL,
    play_url varchar(50) not NULL,
    episode varchar(50) not NULL,
    last_update date not NULL,
    PRIMARY KEY (bangumi_id),
    foreign key (bangumi_id) references bangumi_list(bangumi_id)
    on update cascade
    on delete cascade)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建acfun分表
CREATE TABLE if not exists acfun(
    bangumi_id int not NULL,
    title varchar(50) not NULL,
    play_url varchar(50) not NULL,
    episode varchar(50) not NULL,
    last_update date not NULL,
    PRIMARY KEY (bangumi_id),
    foreign key (bangumi_id) references bangumi_list(bangumi_id)
    on update cascade
    on delete cascade)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建与制作相关的各个表
-- 创建conduct表
create table if not exists conduct(
    -- id自增
    conduct_id int primary key auto_increment,
    conduct_name varchar(50) not null,
    masterpiece varchar(50)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建company表
create table if not exists company(
    -- id自增
    company_id int primary key auto_increment,
    company_name varchar(50) not null,
    masterpiece varchar(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建bangumi_conduct表
create table if not exists bangumi_conduct(
    bangumi_id int not null,
    conduct_id int not null,
    primary key (bangumi_id),
    foreign key (bangumi_id) references bangumi_list(bangumi_id)
    on update cascade
    on delete cascade,
    foreign key (conduct_id) references conduct(conduct_id)
    on update cascade
    on delete cascade
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 创建bangumi_company表
create table if not exists bangumi_company(
    bangumi_id int not null,
    company_id int not null,
    primary key (bangumi_id),
    foreign key (bangumi_id) references bangumi_list(bangumi_id)
    on update cascade
    on delete cascade,
    foreign key (company_id) references company(company_id)
    on update cascade
    on delete cascade
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建cast表
CREATE TABLE if not exists bangumi_cast(
    bangumi_id int not null,
    actor varchar(50) not null,
    primary key (bangumi_id, actor),
    foreign key (bangumi_id) references bangumi_list(bangumi_id)
    on update cascade
    on delete cascade
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建用户表，user_list
create table if not exists user_list(
    if_manager enum('Y','N') not null default 'N',
    user_id int auto_increment,
    name varchar(20) ,
    password varchar(128) not null,
    privilege char(4) not null default 'YNNN',
    primary key(user_id),
    unique key(name)    
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建视图，detail_info
CREATE view detail_info as (
    select bangumi_id, name,company_name,conduct_name,img
    from (((bangumi_list natural join bangumi_company) natural join bangumi_conduct)
	natural join company) natural join conduct
    );

```

### 视图

```mysql
# 作者：杨智麟
# 该视图为用户的番剧的详情信息查询提供便利
# 提供番剧的id,名称，制作公司，头图的信息
-- 创建视图，detail_info
CREATE view detail_info as (
    select bangumi_id, name,company_name,conduct_name,img
    from (((bangumi_list natural join bangumi_company) natural join bangumi_conduct)
	natural join company) natural join conduct
    );
```

### 函数

```mysql
# 函数
# 作者：陈家豪
# 函数作用：ifexist_bili函数作用为，输入bangumi的id，检测其是否在bilibili分表中
#           若存在，则返回id；若不存在，则返回-1.
#           函数ifexist_acfun的作用同上

-- 创建函数，判断id是否存在于某分表中，若不存在则返回-1
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
```

### 触发器

```mysql
# 触发器
# 作者：陈家豪
# 触发器作用为：delete_on_bili: 在bilibili分表上删除某条bangumi信息后，检查其他分表上有无该bangumi信息
#                若其他分表上也没有，则在总表bangumi_list上删除这条bangumi信息。
#                delete_on_acfun的作用同上。

-- 创建触发器
-- 在分表上删除某条目时，检测其在其他分表是否还存在，
-- 若存在则仅删除此条目，不做其他操作
-- 若不存在，则在总表bangumi_list中删除改条目
delimiter //
drop trigger if exists delete_on_bili//
create trigger delete_on_bili
after delete on bilibili
for each row
begin
    if (ifexist_acfun(old.bangumi_id)=-1) then
        begin
            delete from bangumi_list
            where bangumi_list.bangumi_id = old.bangumi_id;
        end;
    end if;
end; //
delimiter ;

delimiter //
drop trigger if exists delete_on_acfun//
create trigger delete_on_acfun
after delete on acfun
for each row
begin
    if (ifexist_bili(old.bangumi_id)=-1) then
        begin
            delete from bangumi_list
            where bangumi_list.bangumi_id = old.bangumi_id;
        end;
    end if;
end; //
delimiter ;
```

### 存储过程

```mysql
# 存储过程
# 作者： 陈家豪
# 存储过程作用：
# insertIntoCompany: 输入动漫id, 名称, 公司名称， 可以将相应信息存储到company、bangumi_company表中
#                    过程： 先判断公司名是否是表中没有的公司，若是则将公司信息插入到company表
#                           再判断bangumi_id是否未录入bangumi_company表中，若未录入，则插入这条信息
# insertIntoConduct: 功能和insertIntoCompany相似

-- 创建存储过程
-- 存储过程insertIntoCompany, 对于一个包含动漫及其制作公司的新条目，首先检验公司是否已存在company表中
-- 若是新的公司，则将公司信息插入company表。
-- 然后将（bangumi_id, company_id）插入到bangumi_company表中
delimiter $$
drop procedure if exists insertIntoCompany $$
create procedure insertIntoCompany(
    in id int,
    in bangumi_name varchar(50),
    in new_company_name varchar(50))
begin
    declare companyId int default 0;
    if new_company_name not in (select company_name from company) then
        begin
        insert into company(company_name,masterpiece)
        values 
        (new_company_name,bangumi_name);
        end;
    end if;
    if id not in (select bangumi_id from bangumi_company) then
        begin
        select company_id into companyId
        from company
        where company.company_name = new_company_name;
        insert into bangumi_company(bangumi_id, company_id)
        values
        (id, companyId);
        end;
    end if;

end$$
delimiter ;


-- 存储过程insertIntoConduct, 对于一个包含动漫及其制作公司的新条目，首先检验公司是否已存在conduct表中
-- 若是新的公司，则将公司信息插入conduct表。
-- 然后将（bangumi_id, conduct_id）插入到bangumi_company表中
delimiter $$
drop procedure if exists insertIntoConduct$$
create procedure insertIntoConduct(in id int,in bangumi_name varchar(50),in new_conduct_name varchar(50))
begin
    declare conductId int default 0;
    if (new_conduct_name not in (select conduct_name from conduct)) then
        begin
        
        insert into conduct(conduct_name,masterpiece)
        values 
        (new_conduct_name,bangumi_name);
        end;
    end if;
    if (id not in (select bangumi_id from bangumi_conduct)) then
        begin
        select conduct_id into conductId
        from conduct
        where conduct.conduct_name = new_conduct_name;
        insert into bangumi_conduct(bangumi_id, conduct_id)
        values
        (id, conductId);
        end;
    end if;
end$$
delimiter ;
```



## 系统实现

### 系统后端

#### 数据库数据维护

通过python爬虫从目标网站中获取数据，插入到数据库中。

##### 番剧更新信息插入/更新：

此处以`bilibili`表为例，`acfun`表同理

爬虫负责从B站中爬取当天更新的番剧信息，对于爬虫获取到的每一条信息，执行如下操作：

1. 检查该番剧是否已经存在于`bilibili`表中，若存在，则仅仅更新最新集数和播放链接，结束该条信息的操作，若不存在，则转到第2步
2. 检查该番剧是否存在于`bangumi_list`总表中，若存在，则仅仅在`bilibili`表中插入该番信息，并保证`id`与`bangumi_list`中对应，结束该条信息操作，若不存在，则转到第3步
3. 在`bangumi_list`中插入该新番剧，在`bilibili`表中插入该新番剧，并保证`id`相同。

##### 番剧详细信息的录入：

从萌娘百科中获取番剧的详细信息。

对于每一条信息，若该番剧存在于总表中，则在监督表、制作公司表、声优表中插入相关数据，并建立关系（此处调用存储过程完成）。

#### 数据库数据CURD接口

##### 数据展示API

`get_last_week`文件，提供了获取一周内的番剧更新信息和番剧详细信息的接口。

###### 一周内番剧信息

关键代码

```python
# 获取一周内的番剧更新信息
def get_last_week():  
    # get bilibili below
    bangumi_list = get_target_week('bilibili')
    result={"result":bangumi_list}
    print('bilibili result')
    print(result)
    # get acfun below
    bangumi_list = get_target_week('acfun')
    # insert acfun into bilibili
    merge_list(result['result'], bangumi_list, 'acfun')
    print('acfun result')
    print(bangumi_list)

    # insert AGE into bilibili
    bangumi_list = get_target_week('AGE')
    merge_list(result['result'], bangumi_list, 'AGE')
    print('AGE result')
    print(bangumi_list)

    print('final result')
    print(result)
    return result

def get_target_week(netName):
    today = datetime.date.today()
    bangumi_list = list()
    for i in range(0,7):
        last_day = today + datetime.timedelta(days= -i)
        weekday = last_day.weekday()
        date = last_day.strftime("%Y-%m-%d")
        list_of_day = get_list_of_date(last_day, netName)
        # solve mysql return void tuble when it is null
        if type(list_of_day) == type(()):
            list_of_day = []
        # update the play_url, make it become a dict
        for i in list_of_day:
            i['play_url'] = {netName: i['play_url']}
        temp = {"date":date,"weekday":weekday,"seasons":list_of_day}
        bangumi_list.append(temp)
    return sorted(bangumi_list, key=lambda keys: keys["weekday"])
```

数据示例

![image-20210605092307676](README.assets/image-20210605092307676.png)

典型界面

![image-20210605092440808](README.assets/image-20210605092440808.png)

###### 番剧详细信息

关键代码

```python
def get_detail_info(id='4100450'):
    db = pymysql.connect(host="localhost", port=3306, db="yukiyu", user="jhchen", password="123456",charset='utf8')
    print('get bangumi detail info: ')
    cursor = db.cursor()
    sql = """
        select * from detail_info
        where bangumi_id = %s
        """%id
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    sql = """
        select actor from bangumi_cast
        where bangumi_id = %s
        """%id
    cursor.execute(sql)
    cast = cursor.fetchall()
    cast = signColumnsShuffle(cast)
    print(cast)
    res = {'result': None}
    if data and cast:
        data = data[0]
        res['result'] = {
            'id':  data[0],
            'name': data[1],
            'company_name': data[2],
            'conduct_name': data[3],
            'img': data[4],
            'cast': cast
        }
    return res
```

数据示例

![image-20210605092555983](README.assets/image-20210605092555983.png)

典型界面

![image-20210605092617592](README.assets/image-20210605092617592.png)

##### 数据管理API

`databaseCURD`文件，提供了数据库增删查改接口，支持对特定表特定条目进行操作。

关键代码

```python
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
def commitChangeToDatabase(oldInfo, newInfo, targetTable, user = None):
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
```

### Web服务

`__init__.py`文件，运行`flask`web微服务，为前端数据展示提供支持。

### 系统前端

采用`H5+Vue`搭建。

#### index页面

欢迎页面，提供登陆、注册入口。

![image-20210605093856905](README.assets/image-20210605093856905.png)

#### main页面

番剧更新时间表展示页面，提供番剧更新时间展示以及番剧详细信息展示。

![image-20210605093915848](README.assets/image-20210605093915848.png)

#### login页面

提供注册和登陆功能。

![image-20210605093934923](README.assets/image-20210605093934923.png)

#### database页面

提供数据库后台管理功能。

![image-20210605094010996](README.assets/image-20210605094010996.png)

![image-20210605094251223](README.assets/image-20210605094251223.png)

### 程序模式图

![program feture graph](README.assets/program feture graph.png)

