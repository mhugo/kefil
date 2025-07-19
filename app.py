from flask import Flask, request, jsonify, send_from_directory
import sqlite3

app = Flask(__name__)

DATABASE = 'orders.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                method TEXT NOT NULL,
                items TEXT NOT NULL,
                total INTEGER NOT NULL
            )
        ''')
        conn.commit()

@app.route('/')
def serve_index():
    return send_from_directory('html', 'index.html')
def list_orders():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders')
        orders = cursor.fetchall()
        return jsonify(orders)

@app.route('/orders', methods=['POST'])
def add_order():
    order_data = request.get_json()
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO orders (timestamp, method, items, total)
            VALUES (?, ?, ?, ?)
        ''', (order_data['timestamp'], order_data['method'], str(order_data['items']), order_data['total']))
        conn.commit()
        return jsonify({'id': cursor.lastrowid}), 201

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
