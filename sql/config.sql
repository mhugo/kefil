delete from categories;
insert into categories (id, name) values (1, 'Crêpes salées');
insert into categories (id, name) values (2, 'Crêpes sucrées');

delete from items;
insert into items (name, preparation_label, category_id, price, grid_x, grid_y, color) values ('Complète', 'OJF', 1, 700, 1, 1, '#0056b3');
insert into items (name, preparation_label, category_id, price, grid_x, grid_y, color) values ('Complète végé', 'OLF', 1, 700, 2, 1, '#0056b3');
insert into items (name, preparation_label, category_id, price, grid_x, grid_y, color) values ('Argoat', 'JF', 1, 600, 1, 2, '#28a745');
insert into items (name, preparation_label, category_id, price, grid_x, grid_y, color) values ('Végé', 'LF ou OF ou OL', 1, 600, 2, 2, '#28a745');
insert into items (name, preparation_label, category_id, price, grid_x, grid_y, color) values ('Simple', '1 ingrédient', 1, 500, 3, 2, '#28a745');
insert into items (name, preparation_label, category_id, price, grid_x, grid_y, color) values ('Confiture', 'K', 2, 400, 1, 3, '#ffc107');
insert into items (name, preparation_label, category_id, price, grid_x, grid_y, color) values ('Chocolat', 'Ch', 2, 400, 2, 3, '#ffc107');
insert into items (name, preparation_label, category_id, price, grid_x, grid_y, color) values ('Caramel', 'Ca', 2, 400, 3, 3, '#ffc107');
insert into items (name, preparation_label, category_id, price, grid_x, grid_y, color) values ('Beurre et/ou Sucre', 'S', 2, 300, 4, 3, '#dc3545');

insert into items (name, category_id, price, batch_quantity, grid_x, grid_y) values ('Crêpes blé noir', 1, 50, 6, 5, 1);
insert into items (name, category_id, price, batch_quantity, grid_x, grid_y) values ('Crêpes froment', 2, 50, 6, 5, 2);

delete from payment_methods;
insert into payment_methods (id, name) values (1, 'Espèces');
insert into payment_methods (id, name) values (2, 'CB');
insert into payment_methods (id, name) values (3, 'Celticash');
