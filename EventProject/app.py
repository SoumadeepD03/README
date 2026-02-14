from flask import Flask, render_template, request,redirect,url_for
import sqlite3
 
app = Flask(__name__)
def get_db_connection():
    # This creates a file named 'database.db' in your folder automatically
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # This lets us access data by column name
    return conn

def init_db():
    conn = get_db_connection()
    # 1. This creates the table if it's missing
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT UNIQUE,password TEXT, role TEXT)')
 
    # 2. This part checks if the table is empty
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        # 3. This inserts a 'Test User' so you can see if the database works!
        conn.execute("INSERT INTO users (username, email, role) VALUES ('Axiom_Admin', 'admin@axiom.com', 'Manager')")
 
    conn.commit()
    conn.close()
 
# MAKE SURE THIS LINE IS HERE to actually run the setup
init_db() 
 

@app.route('/maintain_user')
def maintain_user():
    conn = get_db_connection()
    # This gets everyone from your new 'users' table
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('maintain_user.html', users=users)
 
# This is the home page (Login)
@app.route('/')
def index():
    return render_template('login.html')
 
# This handles where to go after clicking "Login"
# @app.route('/login_logic', methods=['POST'])
# def login_logic():
#     user_id = request.form.get('user_id').lower()
#     # Logic based on your flow chart: Admin, Vendor, or User
#     if user_id == 'admin':
#         return render_template('admin_dashboard.html')
#     elif user_id == 'vendor':
#         return render_template('vendor_dashboard.html')
#     else:
#         return render_template('user_portal.html')

# @app.route('/login_logic', methods=['POST'])
# def login_logic():
#     user_email = request.form.get('user_id').lower() # Taking email from form
 
#     conn = get_db_connection()
#     # Look for this email in your SQLite pantry
#     user = conn.execute('SELECT * FROM users WHERE email = ?', (user_email,)).fetchone()
#     conn.close()
 
#     if user:
#         # If found, open the dashboard
#         return render_template('user_portal.html')
#     else:
#         # If not in database, stay on login or show error
#         return "User not found in database. Please Sign Up."

@app.route('/login_logic', methods=['POST'])
def login_logic():
    # Grab the input from your login.html form
    input_email = request.form.get('user_id').lower() 
    input_password = request.form.get('password') # Make sure name='password' is in your HTML
 
    conn = get_db_connection()
    # Search for a user where BOTH email and password match
    user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', 
                        (input_email, input_password)).fetchone()
    conn.close()
 
    if user:
        # Check their role to decide which dashboard to show
        if user['role'] == 'Admin':
            return render_template('admin_dashboard.html')
        elif user['role'] == 'Vendor':
            return render_template('vendor_dashboard.html')
        else:
            return render_template('user_portal.html')
    else:
        return "Invalid Email or Password. Please try again."
    

@app.route('/products')
def products_page():
    return render_template('products.html')

@app.route('/product_status')
def products_status():
    return render_template('product_status.html')

@app.route('/cart')
def cart_page():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/success')
def success():
    # This matches your "Success" popup (IMG_131011)
    return "<h1>THANK YOU!</h1><p>Order Placed Successfully.</p><button onclick=\"location.href='/'\">Home</button>"

# @app.route('/maintain_user')
# def maintain_user():
#     return render_template('maintain_user.html')

@app.route('/maintain_vendor')
def maintain_vendor():
    return render_template('maintain_vendor.html')

@app.route('/vendor_status')
def vendor_status():
    return render_template('vendor_status.html')
 
@app.route('/update_status')
def update_status():
    return render_template('update_status.html')
 
@app.route('/add_item')
def add_item():
    return render_template('add_item.html')
 
@app.route('/user_management')
def user_management():
    # This matches the "User Management" button in IMG_131112
    return "<h1>User Management</h1><p>Admin can Add or Update Users here.</p><button onclick='history.back()'>Back</button>"

@app.route('/add_membership')
def add_mem():
    return render_template('add_membership.html')

@app.route('/update_membership')
def update_mem():
    return render_template('update_membership.html')
 
@app.route('/success')
def order_success():
    return render_template('success.html')

@app.route('/user_signup')
def user_signup():
    return render_template('user_signup.html')
 
@app.route('/vendor_signup')
def vendor_signup():
    return render_template('vendor_signup.html')


@app.route('/request_item')
def request_item():
    return render_template('request_item.html')

@app.route('/maintain_item')
def maintain_item():
    return render_template('maintain_item.html')

# Route to show the Update page
@app.route('/update_user')
def update_user_page():
    return render_template('update_user.html')
 
# Route to process the update in the database
@app.route('/update_logic', methods=['POST'])
def update_logic():
    user_id = request.form.get('u_id')
    name = request.form.get('new_name')
    email = request.form.get('new_email')
    role = request.form.get('new_role')
    password =request.form.get('u_password')
 
    conn = get_db_connection()
    # Using the SQL UPDATE command to change data for a specific ID
    conn.execute('UPDATE users SET username = ?, email = ?, role = ?, password= ? WHERE id = ?',
                 (name, email, role, password, user_id))
    conn.commit()
    conn.close()
 
    return redirect('/maintain_user')
 
# Route to show the Add User page
@app.route('/add_user')
def add_user_page():
    return render_template('add_user.html')
 
# Route to process the form and save to database
@app.route('/save_user', methods=['POST'])
def save_user():
    # Grab data from the HTML form
    username = request.form.get('u_name')
    email = request.form.get('u_email')
    role = request.form.get('u_role')
    password =request.form.get('u_password')
 
    # Connect to the database and INSERT the data
    conn = get_db_connection()
    conn.execute('INSERT INTO users (username, email, role, password) VALUES (?, ?, ?, ?)',
                 (username, email, role, password))
    conn.commit()
    conn.close()
 
    # Go back to the main table to see the new user
    if role =='User':
        return redirect('/user_portal')
    else:
        return redirect('/maintain_user')


# Route to delete a user by their ID
@app.route('/delete_user/<int:id>')
def delete_user(id):
    conn = get_db_connection()
    # SQL command to remove the specific user
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
 
    # Send the admin back to the table to see it's gone
    return redirect(url_for('maintain_user'))

# Route to process the form and save to database
# @app.route('/signup_user', methods=['POST'])
# def signup_user():
#     # Grab data from the HTML form
#     username = request.form.get('u_name')
#     email = request.form.get('u_email')
#     role = request.form.get('u_role')
#     password =request.form.get('u_password')
 
#     # Connect to the database and INSERT the data
#     conn = get_db_connection()
#     conn.execute('INSERT INTO users (username, email, role, password) VALUES (?, ?, ?, ?)',
#                  (username, email, role, password))
#     conn.commit()
#     conn.close()
 
#     # Go back to the main table to see the new user
#     return redirect('/user_signup')

@app.route('/view_memberships')
def view_memberships():
    conn = get_db_connection()
    # Fetch all rows from your membership table
    memberships = conn.execute('SELECT * FROM memberships').fetchall()
    conn.close()
    # Send the data to your HTML file
    return render_template('view_membership.html', memberships=memberships)
if __name__ == '__main__':
     app.run(debug=True)