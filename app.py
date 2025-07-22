from flask import Flask, request, jsonify, render_template_string
import sqlite3
import json

app = Flask(__name__)

DATABASE = "orders.db"


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                method TEXT NOT NULL,
                total INTEGER NOT NULL
            )
        """
        )

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL
        )
        """
        )

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(item_id) REFERENCES items(id)
        )
        """
        )
        cursor.execute("DELETE FROM order_items")
        cursor.execute("DELETE FROM orders")
        cursor.execute("DELETE FROM items")
        cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", ("Apple", 125))
        cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", ("Banana", 90))
        cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", ("Orange", 150))
        cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", ("Mango", 275))
        cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", ("Grapes", 300))
        cursor.execute(
            "INSERT INTO items (name, price) VALUES (?, ?)", ("Watermelon", 450)
        )
        # Insert sample orders
        cursor.execute(
            "INSERT INTO orders (timestamp, method, total) VALUES (?, ?, ?)",
            ("2025-07-20T12:00:00", "Cash", 365),
        )
        order_id_1 = cursor.lastrowid
        cursor.execute(
            "INSERT INTO order_items (order_id, item_id, quantity) VALUES (?, ?, ?)",
            (order_id_1, 1, 1),
        )  # Apple
        cursor.execute(
            "INSERT INTO order_items (order_id, item_id, quantity) VALUES (?, ?, ?)",
            (order_id_1, 2, 2),
        )  # Banana

        cursor.execute(
            "INSERT INTO orders (timestamp, method, total) VALUES (?, ?, ?)",
            ("2025-07-20T13:00:00", "Card", 450),
        )
        order_id_2 = cursor.lastrowid
        cursor.execute(
            "INSERT INTO order_items (order_id, item_id, quantity) VALUES (?, ?, ?)",
            (order_id_2, 3, 3),
        )  # Orange

        conn.commit()


@app.route("/")
def serve_index():
    with open("html/index.html", "r") as file:
        html_template = file.read()

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM items")
        items = cursor.fetchall()

    items = [{"id": id, "label": name, "price": price} for id, name, price in items]
    return render_template_string(html_template, items_list=items)


@app.route("/orders", methods=["GET"])
def list_orders():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders order by id desc")
        orders = cursor.fetchall()

        order_list = []
        for order in orders:
            order_id, timestamp, method, total = order
            cursor.execute(
                """
                SELECT items.name, items.price, order_items.quantity 
                FROM order_items 
                JOIN items ON order_items.item_id = items.id 
                WHERE order_items.order_id = ?
            """,
                (order_id,),
            )
            items = cursor.fetchall()
            order_list.append(
                {
                    "id": order_id,
                    "timestamp": timestamp,
                    "method": method,
                    "total": total,
                    "items": [
                        {"name": item[0], "price": item[1], "quantity": item[2]}
                        for item in items
                    ],
                }
            )

        return jsonify(order_list)


@app.route("/orders", methods=["POST"])
def add_order():
    order_data = request.get_json()
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (timestamp, method, total) VALUES (?, ?, ?)",
            (order_data["timestamp"], order_data["method"], order_data["total"]),
        )
        order_id = cursor.lastrowid

        for item in order_data["items"]:
            cursor.execute(
                "INSERT INTO order_items (order_id, item_id, quantity) VALUES (?, ?, ?)",
                (order_id, item["id"], item["quantity"]),
            )
        conn.commit()
        return jsonify({"id": cursor.lastrowid}), 201


@app.route("/summary", methods=["GET"])
def get_summary():
    date = request.args["date"]
    print(f"date: {date}")

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "select count(*) as n_orders, sum(total) as total from orders where date(timestamp) = ?",
            (date,),
        )
        n_orders, total = cursor.fetchone()

    with open("html/summary.html", "r") as file:
        html_template = file.read()

    return render_template_string(
        html_template, n_orders=n_orders or 0, total=total or 0
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
