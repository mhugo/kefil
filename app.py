from flask import Flask, request, jsonify, render_template_string, send_from_directory
import sqlite3
import json

app = Flask(__name__)

DATABASE = "orders.db"


@app.route("/")
def serve_index():
    with open("html/index.html", "r") as file:
        html_template = file.read()

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM items")
        items = cursor.fetchall()
        cursor.execute("SELECT id, name FROM payment_methods")
        payment_methods = cursor.fetchall()

    items = [{"id": id, "label": name, "price": price} for id, name, price in items]
    payment_methods = {id: name for id, name in payment_methods}
    return render_template_string(
        html_template, items_list=items, payment_methods=payment_methods
    )


@app.route("/html_summary")
def serve_summary():
    return send_from_directory("html", "summary.html")


@app.route("/html_history")
def serve_history():
    return send_from_directory("html", "history.html")


@app.route("/common.css")
def serve_css():
    return send_from_directory("html", "common.css")


@app.route("/orders", methods=["GET"])
def list_orders():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            select o.id, timestamp, p.name, total from orders o, payment_methods p
            where p.id = o.method_id order by o.id desc
            """
        )
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
        timestamp = order_data["timestamp"]
        cursor.execute(
            "select max(id_in_day) from orders where date(timestamp) = date(?)",
            (timestamp,),
        )
        last_id = cursor.fetchone()[0] or 0
        cursor.execute(
            "INSERT INTO orders (id_in_day, timestamp, method_id, total) VALUES (?, ?, ?, ?)",
            (last_id + 1, timestamp, order_data["method_id"], order_data["total"]),
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

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "select count(*) as n_orders, sum(total) as total, max(id_in_day) as last_id from orders where date(timestamp) = ?",
            (date,),
        )
        n_orders, total, last_id = cursor.fetchone()

        cursor.execute(
            "select sum(oi.quantity) from orders o, order_items oi where oi.order_id = o.id and date(o.timestamp) = ?",
            (date,),
        )
        n_items = cursor.fetchone()[0]

        # count by category
        cursor.execute(
            """
            select
              c.name, sum(oi.quantity)
            from
              order_items oi,
              orders o,
              items i,
              categories c
            where
              oi.order_id = o.id
              and oi.item_id = i.id
              and i.category_id = c.id
              and date(o.timestamp) = ?
            group by
              i.category_id
            """,
            (date,),
        )

        count_per_category = {r[0]: r[1] for r in cursor.fetchall()}

        # Count per item
        cursor.execute(
            """
            select
              i.name,
              sum(oi.quantity)
            from
              order_items oi,
              orders o,
              items i
            where
              oi.order_id = o.id
              and oi.item_id = i.id
              and date(o.timestamp) = ?
            group by i.id
            """,
            (date,),
        )
        count_per_item = {r[0]: r[1] for r in cursor.fetchall()}

    summary = {
        "n_orders": n_orders or 0,
        "n_items": n_items or 0,
        "total": total or 0,
        "last_id": last_id or 0,
        "count_per_category": count_per_category or {},
        "count_per_item": count_per_item or {},
    }

    if "application/json" in request.headers.get("accept", ""):
        return jsonify(summary)
    else:
        with open("html/summary.parts.html", "r") as file:
            html_template = file.read()
            return render_template_string(html_template, summary=summary)


@app.route("/voucher", methods=["GET", "POST"])
def get_voucher():
    if request.method == "GET":
        id = (request.args.get("id", "")).upper()
    elif request.method == "POST":
        id = request.get_json().get("id", "").upper()

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "select id, description, origin, is_consumed, consumption_timestamp from vouchers where id = ?",
            (id,),
        )
        row = cursor.fetchone()
        if row is not None:
            id, description, origin, is_consumed, consumption_ts = row
            state = {
                "id": id,
                "description": description,
                "origin": origin,
                "is_consumed": bool(is_consumed),
                "consumption_ts": consumption_ts,
            }
            if request.method == "GET":
                return jsonify(state)
            elif request.method == "POST":
                if not is_consumed:
                    state["is_consumed"] = True
                    cursor.execute(
                        """
                      update vouchers
                      set
                        is_consumed=true,
                        consumption_timestamp=datetime('now','localtime')
                      where id=?
                      returning consumption_timestamp
                    """,
                        (id,),
                    )
                    state["consumption_ts"] = cursor.fetchone()[0]
                return jsonify(state)

        else:
            return "Voucher not found", 400


if __name__ == "__main__":
    app.run(debug=True)
