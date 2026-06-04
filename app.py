import datetime
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
        cursor.execute(
            "SELECT id, parent_id, name, price, batch_quantity, grid_x, grid_y, color FROM items"
        )
        items = cursor.fetchall()
        cursor.execute("SELECT id, name FROM payment_methods")
        payment_methods = cursor.fetchall()

    all_items = {
        id: {
            "id": id,
            "parent_id": parent_id,
            "label": name,
            "price": price,
            "batch_quantity": batch_quantity or 1,
            "grid_x": grid_x,
            "grid_y": grid_y,
            "bg_color": color or "#fff",
            "color": "#fff" if color else "#007bff",
        }
        for id, parent_id, name, price, batch_quantity, grid_x, grid_y, color in items
    }

    for id, item in all_items.items():
        parent_id = item["parent_id"]
        if parent_id is not None:
            parent = all_items[parent_id]
            parent.setdefault("sub_menu", {}).setdefault("items", []).append(item)

    items = [item for _, item in all_items.items() if item["parent_id"] is None]

    items_str = json.dumps(items)
    print(json.dumps(items, indent=2))

    payment_methods = {id: name for id, name in payment_methods}
    return render_template_string(
        html_template,
        items_list=items_str,
        payment_methods=payment_methods,
        enable_discount=int(config.get("enable_discount", "0")),
        enable_voucher=int(config.get("enable_voucher", "0")),
        add_simple_validation=int(config.get("add_simple_validation", "0")),
    )


@app.route("/html_summary")
def serve_summary():
    date = request.args.get("date") or datetime.datetime.now().date().isoformat()

    summary = fetch_summary(date)

    previous_date = (
        datetime.date.fromisoformat(date) - datetime.timedelta(days=1)
    ).isoformat()
    next_date = (
        datetime.date.fromisoformat(date) + datetime.timedelta(days=1)
    ).isoformat()
    with open("html/summary.html", "r") as file:
        html_template = file.read()
    return render_template_string(
        html_template,
        summary=summary,
        current_date=date,
        previous_date=previous_date,
        next_date=next_date,
    )


@app.route("/html_history")
def serve_history():
    date = request.args.get("date") or datetime.datetime.now().date().isoformat()
    previous_date = (
        datetime.date.fromisoformat(date) - datetime.timedelta(days=1)
    ).isoformat()
    next_date = (
        datetime.date.fromisoformat(date) + datetime.timedelta(days=1)
    ).isoformat()
    with open("html/history.html", "r") as file:
        html_template = file.read()
    return render_template_string(
        html_template,
        current_date=date,
        previous_date=previous_date,
        next_date=next_date,
    )


@app.route("/common.css")
def serve_css():
    return send_from_directory("html", "common.css")


def fetch_order_items(cursor, order_id: int):
    cursor.execute("select id_in_day from orders where id = ?", (order_id,))
    id_in_day = cursor.fetchone()[0]
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
    return {
        "id": order_id,
        "id_in_day": id_in_day,
        "items": [
            {"name": name, "price": price, "quantity": quantity}
            for name, price, quantity in items
        ],
    }


@app.route("/order_items", methods=["GET"])
def order_items():
    order_id = request.args["id"]
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        order_items = fetch_order_items(cursor, order_id)
        return jsonify(order_items)


@app.route("/print_order_items", methods=["GET"])
def print_order_items():
    from printer import print_order

    order_id = request.args["id"]
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        order = fetch_order_items(cursor, order_id)
        print_order(order)
        return "Ok", 200


@app.route("/orders", methods=["GET"])
def list_orders():
    date = request.args["date"]
    limit = request.args.get("limit")
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            select o.id, o.id_in_day, timestamp, p.name, total, discount from orders o, payment_methods p
            where p.id = o.method_id and date(timestamp) = ? order by o.id desc
            """
            + (f"limit {limit}" if limit is not None else ""),
            (date,),
        )
        orders = cursor.fetchall()

        order_list = []
        for order in orders:
            order_id, id_in_day, timestamp, method, total, discount = order
            order_items = fetch_order_items(cursor, order_id)
            order_list.append(
                {
                    "id": order_id,
                    "id_in_day": id_in_day,
                    "timestamp": timestamp,
                    "method": method,
                    "discount": discount,
                    "total": total,
                    "items": order_items,
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
            "INSERT INTO orders (id_in_day, timestamp, method_id, total, discount) VALUES (?, ?, ?, ?, ?)",
            (
                last_id + 1,
                timestamp,
                order_data["method_id"],
                order_data["total"],
                order_data["discount"],
            ),
        )
        order_id = cursor.lastrowid

        for item in order_data["items"]:
            cursor.execute(
                "INSERT INTO order_items (order_id, item_id, quantity) VALUES (?, ?, ?)",
                (order_id, item["id"], item["quantity"]),
            )
        conn.commit()
        return jsonify({"id": order_id}), 201


def fetch_summary(date: str):
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

        cursor.execute(
            """
            select
              m.name, sum(total)
            from
              orders o, payment_methods m
            where
              m.id = o.method_id and
              date(timestamp)=?
            group by method_id
            """,
            (date,),
        )
        total_per_payment_method = {r[0]: r[1] for r in cursor.fetchall()}

    return {
        "n_orders": n_orders or 0,
        "n_items": n_items or 0,
        "total": total or 0,
        "last_id": last_id or 0,
        "count_per_category": count_per_category or {},
        "count_per_item": count_per_item or {},
        "total_per_payment_method": total_per_payment_method or {},
    }


@app.route("/summary", methods=["GET"])
def get_summary():
    date = request.args["date"]

    summary = fetch_summary(date)

    return jsonify(summary)


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
