delete from categories;
insert into categories (id, name) values (1, 'Crêpes salées');
insert into categories (id, name) values (2, 'Crêpes sucrées');

delete from items;
insert into items (id, name, category_id, price, grid_x, grid_y, color) values (1, 'BN 1 ingrédient', 1, 0, 1, 1, '#327ba8');
insert into items (id, name, category_id, price, grid_x, grid_y, color) values (2, 'BN 2 ingrédients', 1, 0, 2, 1, '#195c85');
insert into items (id, name, category_id, price, grid_x, grid_y, color) values (3, 'BN 3 ingrédients', 1, 0, 3, 1, '#405461');
insert into items (id, name, category_id, price, grid_x, grid_y, color) values (4, 'Froment', 2, 0, 1, 2, '#ab4f27');
insert into items (id, name, category_id, price, grid_x, grid_y, color) values (5, 'Nues', 2, 0, 1, 3, null);

insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (1, 'Jambon', 1, 300, 1, 1, '#915687');
insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (1, 'Oeuf', 1, 300, 2, 1, '#ffc107');
insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (1, 'Fromage', 1, 300, 2, 2, '#c99716');
insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (1, 'Légumes', 1, 300, 1, 2, '#28a745');
insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (1, 'Beurre BN', 1, 200, 1, 3, '#8a8154');

insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (2, 'Jambon / Fromage', 1, 400, 1, 1, '#28a745');
insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (2, 'Oeuf / Fromage', 1, 400, 2, 1, '#28a745');
insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (2, 'Jambon / Oeuf', 1, 400, 3, 1, '#28a745');
insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (2, 'Légumes / Oeuf', 1, 400, 1, 2, '#28a745');
insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (2, 'Légumes / Fromage', 1, 400, 2, 2, '#28a745');
insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (2, 'Légumes / Jambon', 1, 400, 3, 2, '#28a745');

insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (3, 'Complète (O/J/F)', 1, 500, 1, 1, '#28a745');
insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (3, 'Complète végé (O/F/L)', 1, 500, 2, 1, '#28a745');
insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (3, 'Jambon / Oeuf / Légumes', 1, 400, 1, 2, '#28a745');
insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (3, 'Jambon / Fromage / Légumes', 1, 400, 2, 2, '#28a745');

insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (4, 'Chocolat', 2, 300, 1, 1, '#c4a137');
insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (4, 'Caramel', 2, 300, 2, 1, '#c4a137');
insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (4, 'Confiture', 2, 300, 3, 1, '#c4a137');
insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (4, 'Beurre / Sucre', 2, 250, 2, 2, '#c4a137');
insert into items (parent_id, name, category_id, price, grid_x, grid_y, color) values (4, 'Beurre FR', 2, 200, 1, 2, '#8a8154');

insert into items (parent_id, name, category_id, price, batch_quantity, grid_x, grid_y) values (5, '6x Crêpes BN', 1, 50, 6, 1, 1);
insert into items (parent_id, name, category_id, price, batch_quantity, grid_x, grid_y) values (5, '6x Crêpes FR', 2, 50, 6, 1, 2);

delete from payment_methods;
insert into payment_methods (id, name) values (1, 'Ticket');
insert into payment_methods (id, name) values (2, 'Espèces');
insert into payment_methods (id, name) values (3, 'CB');

delete from config;
insert into config (key, value) values ('default_payment_id', 1);
insert into config (key, value) values ('default_payment_name', (select name from payment_methods where id=(select value from config where key='default_payment_id')));
insert into config (key, value) values ('enable_discount', false);
insert into config (key, value) values ('enable_voucher', false);
insert into config (key, value) values ('add_simple_validation', false);
