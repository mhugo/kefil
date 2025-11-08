delete from categories;
insert into categories (id, name) values (1, 'Crêpes salées');
insert into categories (id, name) values (2, 'Crêpes sucrées');

delete from items;
insert into items (name, category_id, price, grid_x, grid_y, color) values ('Complète', 1, 500, 1, 1, '#0056b3');

insert into items (name, category_id, price, grid_x, grid_y, color) values ('Jambon/Fromage', 1, 400, 1, 2, '#28a745');
insert into items (name, category_id, price, grid_x, grid_y, color) values ('Oeuf/Fromage', 1, 400, 2, 2, '#28a745');
insert into items (name, category_id, price, grid_x, grid_y, color) values ('Jambon/Oeuf', 1, 400, 3, 2, '#28a745');

insert into items (name, category_id, price, grid_x, grid_y, color) values ('Beurre BN', 1, 250, 2, 1, '#dc3545');
insert into items (name, category_id, price, grid_x, grid_y, color) values ('Beurre FR', 2, 200, 3, 1, '#dc3545');

insert into items (name, category_id, price, grid_x, grid_y, color) values ('Chocolat', 2, 300, 1, 3, '#ffc107');
insert into items (name, category_id, price, grid_x, grid_y, color) values ('Caramel', 2, 300, 2, 3, '#ffc107');
insert into items (name, category_id, price, grid_x, grid_y, color) values ('Beurre/Sucre', 2, 200, 3, 3, '#ffc107');

insert into items (name, category_id, price, batch_quantity, grid_x, grid_y) values ('6x Crêpes BN', 1, 50, 6, 5, 1);
insert into items (name, category_id, price, batch_quantity, grid_x, grid_y) values ('6x Crêpes FR', 2, 50, 6, 5, 2);

delete from payment_methods;
insert into payment_methods (id, name) values (1, 'Celticash');
insert into payment_methods (id, name) values (2, 'Espèces');
insert into payment_methods (id, name) values (3, 'CB');
