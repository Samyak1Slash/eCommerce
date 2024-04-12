from flask import Flask
from flask import render_template
from flask import request
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

# Route to form used to add a new product to the database
@app.route("/enternew")
def enternew():
    return render_template("index.html")

# Route to add a new record (INSERT) product data to the database
@app.route("/addrec", methods = ['POST', 'GET'])
def addrec():
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            prc = request.form['price']

            # Connect to SQLite3 database and execute the INSERT
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO List (product_nm,product_prc) VALUES (?,?)",(nm, prc))

                con.commit()
                msg = "Record successfully added to database"
        except:
            con.rollback()
            msg = "Error in the INSERT"

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)



@app.route("/add/product")
def addproduct():
    return render_template("Add_productByowner.html")



# @app.route('/list')
# def list():
#     # Connect to the SQLite3 datatabase and 
#     # SELECT rowid and all Rows from the products table.
#     con = sqlite3.connect("database.db")
#     con.row_factory = sqlite3.Row

#     cur = con.cursor()
#     cur.execute("SELECT rowid, * FROM products")

#     rows = cur.fetchall()
#     total_price = calculate_total_price()
#     con.close()
#     # Send the results of the SELECT to the list.html page
#     return render_template("list.html",rows=rows,total_price=total_price)
# def calculate_total_price():
#     conn = sqlite3.connect('database.db')
#     cur = conn.cursor()
#     cur.execute("SELECT SUM(product_price) FROM Products")
#     total_price = cur.fetchone()[0]  # Fetch the total price
#     conn.close()
#     return total_price

# Route that will SELECT a specific row in the database then load an Edit form 
@app.route("/edit", methods=['POST','GET'])
def edit():
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            id = request.form['id']
            # Connect to the database and SELECT a specific rowid
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT rowid, * FROM products WHERE rowid = " + id)

            rows = cur.fetchall()
        except:
            id=None
        finally:
            con.close()
            # Send the specific record of data to edit.html
            return render_template("edit.html",rows=rows)

# Route used to execute the UPDATE statement on a specific record in the database
@app.route("/editrec", methods=['POST','GET'])
def editrec():
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['rowid']
            nm = request.form['nm']
            prc = request.form['prc']

            # UPDATE a specific record in the database based on the rowid
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE products SET name='"+nm+"', price='"+prc+"' WHERE rowid="+rowid)

                con.commit()
                msg = "Record successfully edited in the database"
        except:
            con.rollback()
            msg = "Error in the Edit: UPDATE products SET name="+nm+", price="+prc+" WHERE rowid="+rowid

        finally:
            con.close()
            return render_template('result.html',msg=msg)

@app.route("/delete", methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        try:
             # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['id']
            # Connect to the database and DELETE a specific record based on rowid
            with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute("DELETE FROM products WHERE rowid="+rowid)

                    con.commit()
                    msg = "Record successfully deleted from the database"
        except:
            con.rollback()
            msg = "Error in the DELETE"

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)


@app.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        try:
            search_query = request.form['search_query']
            
            # Connect to the database
            conn = sqlite3.connect('database.db')
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            # Adjust the query to search specifically for the entered text in the name column
            cur.execute("SELECT * FROM List WHERE product_nm LIKE ?", ('%' + search_query + '%',))
            rows = cur.fetchall()
            conn.close()
            if rows:
                return render_template('search_results.html', rows=rows)
            else:
                return render_template('no_product_found.html')
        except Exception as e:
            return render_template('error.html', error=str(e))
    else:
        return render_template('search_form.html')




@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    
    name = request.json['name']
    price = request.json['price']
    
    # Add the item to your cart (database) here
    with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO products (product_name,product_price) VALUES (?,?)",(name, price))

                con.commit()
                con.close()
                
    
    return 'Item added to cart', 200



@app.route('/checkout', methods=['POST'])
def checkout():
    rows = get_all_products()
    total_price = calculate_total_price() 
    delete_all_products()  # Delete all products after checkout
    if rows:
        return render_template("checkout.html", rows=rows, total_price=total_price)
    else:
        return render_template('no_product_found.html')

def get_all_products():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM products")
    rows = cur.fetchall()
    con.close()
    return rows

def calculate_total_price():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT SUM(product_price) FROM Products")
    total_price = cur.fetchone()[0] or 0  # Fetch the total price or set to 0 if NULL
    conn.close()
    return total_price

def delete_all_products():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM Products")
    conn.commit()
    conn.close()

@app.route('/list')
def list():
    rows = get_all_products()
    total_price = calculate_total_price()
    return render_template("list.html", rows=rows, total_price=total_price)



if __name__=="__main__":# basically we are telling the code to run
    app.run(debug=True,port=5757)