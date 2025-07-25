delete from order_items;
delete from orders;

insert into orders (id, id_in_day, timestamp, method_id, total)
  select 1, 1, datetime('now'), (select id from payment_methods where name='CB'), 800;
insert into order_items (order_id, item_id, quantity)
  select 1, (select id from items where name='Chocolat'), 2;

insert into orders (id, id_in_day, timestamp, method_id, total)
  select 2, 2, datetime('now'), (select id from payment_methods where name='Celticash'), 1100;
insert into order_items (order_id, item_id, quantity)
  select 2, (select id from items where name='Chocolat'), 1;
insert into order_items (order_id, item_id, quantity)
  select 2, (select id from items where name='Complète'), 1;

insert into orders (id, id_in_day, timestamp, method_id, total)
  select 3, 3, datetime('now'), (select id from payment_methods where name='Espèces'), 1200;
insert into order_items (order_id, item_id, quantity)
  select 3, (select id from items where name='Argoat'), 1;
insert into order_items (order_id, item_id, quantity)
  select 3, (select id from items where name='Végé'), 1;

delete from vouchers;
insert into vouchers (id, description, is_consumed)
  values ('ABC12', 'Une crêpe gratuite', false);
insert into vouchers (id, description, is_consumed)
  values ('XYZ34', 'Une crêpe gratuite', false);



