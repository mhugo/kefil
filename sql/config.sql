delete from categories;
insert into categories (id, name) values (1, 'Crêpes salées');
insert into categories (id, name) values (2, 'Crêpes sucrées');

delete from items;
insert into items (name, preparation_label, category_id, price) values ('Complète', 'OJF', 1, 700);
insert into items (name, preparation_label, category_id, price) values ('Complète végé', 'OLF', 1, 700);
insert into items (name, preparation_label, category_id, price) values ('Argoat', 'JF', 1, 600);
insert into items (name, preparation_label, category_id, price) values ('Végé', 'LF ou OF ou OL', 1, 600);
insert into items (name, preparation_label, category_id, price) values ('Simple', '1 ingrédient', 1, 500);
insert into items (name, preparation_label, category_id, price) values ('Confiture', 'K', 2, 400);
insert into items (name, preparation_label, category_id, price) values ('Chocolat', 'Ch', 2, 400);
insert into items (name, preparation_label, category_id, price) values ('Caramel', 'Ca', 2, 400);
insert into items (name, preparation_label, category_id, price) values ('Beurre et/ou Sucre', 'S', 2, 300);

insert into items (name, category_id, price, batch_quantity) values ('Crêpes blé noir sèches', 1, 50, 6);
insert into items (name, category_id, price, batch_quantity) values ('Crêpes froment sèches', 2, 50, 6);

delete from payment_methods;
insert into payment_methods (id, name) values (1, 'Espèces');
insert into payment_methods (id, name) values (2, 'CB');
insert into payment_methods (id, name) values (3, 'Celticash');
