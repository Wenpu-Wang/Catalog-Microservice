drop database if exists catalog_db;
create database catalog_db;

# Create tables for catalog_db
use catalog_db;

create table if not exists item_info
(
    id     int auto_increment primary key,
    `name`   varchar(128) not null,
    `description`    varchar(128) not null,
    item_price      double not null,
    image_url       varchar(2083),
    constraint unique_name unique (`name`)
);

create table if not exists item_stocking
(
  item_id int auto_increment not null primary key,
  stock int not null,
  foreign key (item_id) references item_info(id)
);

# Insert sample data for tables for table item_info
use catalog_db;
# alter table item_info add constraint unique_name unique(name);

insert into item_info
(name, description, item_price)
values
('Coca Cola', 'Coke product 500ml from Coca Cola', 2.5),
('Pepsi Coke', 'Coke product 500ml from Pepsi', 2.5),
('Orange Juice', 'Orange juice 500ml with pulp', 5),
('Apple Juice', 'Apple Juice 500ml no pulp', 5),
('Eggs Brown Large Grade A, 12 Count', 'Eggs pack, 12 count', 3.39),
('PS5', 'Gaming console from Sony', 449.99),
('Nintendo Switch', 'Gaming console from Nintendo', 299),
('Xbox Series X', 'Gaming console from Microsoft', 499),
('Salmon Sashimi', 'Fresh salmon sashimi + tax', 12.25),
('Octopus Sashimi', 'Fresh octopus sashimi + tax', 11.25);

insert into item_stocking
(stock)
values
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10);


# # test delete and insert back
# delete from item_stocking where item_id = 9;
# delete from item_info where id = 21;
#
# insert into item_info (id, name, description, item_price)
# values (9, 'Salmon Sashimi', 'Fresh salmon sashimi + tax', 12.25);
#
# insert into item_stocking (item_id, stock) values (9, 9);
#
# # test insert new item
# insert into item_info (id, name, description, item_price)
# values (25, 'Test Item', 'Test Item for test', 999);
# insert into item_stocking (item_id, stock) values (25, 100);

