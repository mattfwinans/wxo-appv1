from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('vendors.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor TEXT NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Route to render the front-end
@app.route('/')
def index():
    return render_template('index.html')

# Create a new entry
@app.route('/api/vendors', methods=['POST'])
def create_vendor():
    data = request.get_json()
    vendor = data['vendor']
    price = data['price']
    date = data.get('date', datetime.now().strftime('%Y-%m-%d'))

    conn = sqlite3.connect('vendors.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vendors (vendor, price, date) VALUES (?, ?, ?)", (vendor, price, date))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Vendor added successfully'}), 201

# Read all entries
@app.route('/api/vendors', methods=['GET'])
def get_vendors():
    conn = sqlite3.connect('vendors.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vendors")
    rows = cursor.fetchall()
    conn.close()

    vendors = [{'id': row[0], 'vendor': row[1], 'price': row[2], 'date': row[3]} for row in rows]
    return jsonify(vendors)

# Update an entry
@app.route('/api/vendors/<int:vendor_id>', methods=['PUT'])
def update_vendor(vendor_id):
    data = request.get_json()
    vendor = data.get('vendor')
    price = data.get('price')
    date = data.get('date')

    conn = sqlite3.connect('vendors.db')
    cursor = conn.cursor()
    if vendor:
        cursor.execute("UPDATE vendors SET vendor = ? WHERE id = ?", (vendor, vendor_id))
    if price:
        cursor.execute("UPDATE vendors SET price = ? WHERE id = ?", (price, vendor_id))
    if date:
        cursor.execute("UPDATE vendors SET date = ? WHERE id = ?", (date, vendor_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Vendor updated successfully'})

# Delete an entry
@app.route('/api/vendors/<int:vendor_id>', methods=['DELETE'])
def delete_vendor(vendor_id):
    conn = sqlite3.connect('vendors.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vendors WHERE id = ?", (vendor_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Vendor deleted successfully'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
