-- 请登入mysql后输入 source D:/yukiyu/flaskr/dbinit.sql的完整路径
drop database if exists yukiyu;

create database if not exists yukiyu
default character set utf8
default collate utf8_general_ci;

use yukiyu

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


-- 函数与触发器

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

-- root
insert into user_list(if_manager,name,password,privilege)
values('Y','root','pbkdf2:sha256:260000$JsFZVWr6NczKuYpn$a97193b04f5fee5307f226bb66394b1e8bec80341f2f127b6e2df78891de56a4','YYYY');