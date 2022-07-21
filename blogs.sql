create database blog;
use blog;

create table user(
	id int primary key auto_increment,
    name varchar(60) not null,
    username varchar(50) not null,
    email varchar(70) not null,
    password varchar(200) not null,
    created_at date not null
);

create table entrada(
    id int primary key auto_increment,
    user_id int not null,
    title varchar(100) not null,
    description varchar(100) not null,
    img varchar(300) not null,
    created_at date not null,
    url varchar(150) not null,
    blog text(60000) not null,
    foreign key(user_id) references user (id)
);

select * from user;
drop table entradas;
select * from entrada;

select e.id, e.title, u.username,e.description, e.img, e.created_at, e.url from entrada e left join user u on u.id = e.user_id;