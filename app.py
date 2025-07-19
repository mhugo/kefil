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
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(item_id) REFERENCES items(id)
        )
        ''')
        conn.commit()

@app.route('/')
def serve_index():
    return send_from_directory('html', 'index.html')
@app.route('/orders', methods=['GET'])
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
        cursor.execute('INSERT INTO orders (timestamp, method, total) VALUES (?, ?, ?)',
                       (order_data['timestamp'], order_data['method'], order_data['total']))
        order_id = cursor.lastrowid

        for item in order_data['items']:
            cursor.execute('INSERT INTO order_items (order_id, item_id, quantity) VALUES (?, ?, ?)',
                           (order_id, item['id'], item['quantity']))
        conn.commit()
        return jsonify({'id': cursor.lastrowid}), 201

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
