# app.py
from flask import Flask, render_template, request, send_file
import sqlite3
import xlwt
import io
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'


def get_db_connection():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    message = None
    user_purchases = []

    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        name = request.form['name']
        selected_products = request.form.getlist('product')

        conn.execute("INSERT OR IGNORE INTO users (id, name) VALUES (?, ?)", (user_id, name))

        total = 0
        for pid in selected_products:
            product = conn.execute("SELECT name, price FROM products WHERE id = ?", (pid,)).fetchone()
            if product:
                conn.execute('''
                    INSERT INTO purchases (user_id, product_id, product_name, price)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, pid, product['name'], product['price']))
                total += product['price']

        conn.commit()

        user_purchases = conn.execute('''
            SELECT product_name, price
            FROM purchases
            WHERE user_id = ?
        ''', (user_id,)).fetchall()

        message = f"Purchase recorded. Total cost: ${total:.2f}"

    conn.close()
    return render_template('index1.html', products=products, message=message, purchases=user_purchases)


@app.route('/export')
def export():
    conn = get_db_connection()
    data = conn.execute('''
        SELECT u.id as user_id, u.name, p.name as product_name, pur.price
        FROM purchases pur
        JOIN users u ON pur.user_id = u.id
        JOIN products p ON pur.product_id = p.id
        ORDER BY u.id
    ''').fetchall()

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Purchases')

    headers = ['User ID', 'User Name', 'Product', 'Price']
    for col, h in enumerate(headers):
        ws.write(0, col, h)

    for row_num, row in enumerate(data, start=1):
        ws.write(row_num, 0, row['user_id'])
        ws.write(row_num, 1, row['name'])
        ws.write(row_num, 2, row['product_name'])
        ws.write(row_num, 3, row['price'])

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(output, download_name="purchase_summary.xls", as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
