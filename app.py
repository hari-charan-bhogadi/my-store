from flask import Flask, render_template, request, redirect
import sqlite3, os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price TEXT, image TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        image = request.files['image']

        if image:
            path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(path)

            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("INSERT INTO products (name, price, image) VALUES (?, ?, ?)",
                      (name, price, path))
            conn.commit()
            conn.close()

        return redirect('/')

    return render_template('add.html')

app.run(debug=True)