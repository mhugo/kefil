CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    preparation_label TEXT,
    batch_quantity INTEGER,
    price INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    grid_x INTEGER,
    grid_y INTEGER,
    color TEXT,
    FOREIGN KEY(category_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS payment_methods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_in_day INTEGER,
    timestamp TEXT NOT NULL,
    method_id INTEGER NOT NULL,
    total INTEGER NOT NULL,
    discount INTEGER,
    FOREIGN KEY(method_id) REFERENCES payment_methods(id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(item_id) REFERENCES items(id)
);

create table if not exists vouchers (
       id varchar(5) primary key,
       description text,
       origin text,
       is_consumed boolean not null,
       consumption_timestamp text
);
