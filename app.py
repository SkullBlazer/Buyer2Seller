from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Iwonttellany1!"
app.config['MYSQL_DB'] = "test"
db = MySQL(app)
login = False

@app.route('/login', methods=['GET', 'POST'])
def index():
    global login
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM buyer;")
        bid = cur.rowcount + 1
        try:
            pincode = request.form['pin']
            email = request.form['email']
            cur.execute('INSERT INTO buyer (bid, bname, email, bpass, pincode) VALUES\
            (%s, %s, %s, %s, %s);', (bid, username, email, password, pincode))
        except KeyError:
            cur.execute('SELECT * FROM buyer WHERE bname = %s AND bpass = %s;', (username, password))
            cur.fetchall()
            if cur.rowcount == 0:
                return "Invalid Name and/or Password."
            else:
                login = True
                return redirect(url_for('logged_in'))
        db.connection.commit()
        cur.close()
        return "Success!"
    return render_template('index.html')

@app.route('/users')
def users():
    cur = db.connection.cursor()
    users = cur.execute("SELECT * FROM buyer;")

    if users > 0:
        userDetails = cur.fetchall()
        return render_template('users.html', userDetails=userDetails)
    cur.close()

@app.route('/u')
def logged_in():
    if login:
        return render_template('site2.html')
    else:
        return redirect(url_for('index'))

@app.route('/home')
def home():
    global login
    if login:
        return render_template('site2.html')
    else:
        return render_template('site.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/seller', methods=['GET', 'POST'])
def sell():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        address = request.form['addr1'] + ', ' + request.form['addr2']
        phone = request.form['phone']
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM seller;")
        sid = cur.rowcount + 1
        cur.execute('INSERT INTO seller (sid, sname, email, spass, phone, address)\
             VALUES (%s, %s, %s, %s, %s, %s);', (sid, username, email, password, phone, address))
        db.connection.commit()
        cur.close()
    return render_template('seller.html')

@app.route('/')
def redir():
    return redirect(url_for('home'))

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route('/product/1')
def product1():
    return render_template('products/product1.html')

@app.route('/product/2')
def product2():
    return render_template('products/product2.html')

@app.route('/product/3')
def product3():
    return render_template('products/product3.html')

@app.route('/product/4')
def product4():
    return render_template('products/product4.html')

@app.route('/product/5')
def product5():
    return render_template('products/product5.html')

@app.route('/product/6')
def product6():
    return render_template('products/product6.html')

@app.route('/sdetails/1')
def sdetails1():
    return render_template('details/details1.html')

@app.route('/sdetails/2')
def sdetails2():
    return render_template('details/details2.html')

@app.route('/sdetails/3')
def sdetails3():
    return render_template('details/details3.html')

if __name__ == "__main__":
    app.run(debug=True)