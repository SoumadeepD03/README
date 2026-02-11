from flask import Flask, render_template, request
 
app = Flask(__name__)
 
# This is the home page (Login)
@app.route('/')
def index():
    return render_template('login.html')
 
# This handles where to go after clicking "Login"
@app.route('/login_logic', methods=['POST'])
def login_logic():
    user_id = request.form.get('user_id').lower()
    # Logic based on your flow chart: Admin, Vendor, or User
    if user_id == 'admin':
        return render_template('admin_dashboard.html')
    elif user_id == 'vendor':
        return render_template('vendor_dashboard.html')
    else:
        return render_template('user_portal.html')

@app.route('/products')
def products_page():
    return render_template('products.html')

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

@app.route('/maintain_user')
def maintain_user():
    return render_template('maintain_user.html')

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
 
@app.route('/success')
def order_success():
    return render_template('success.html')

@app.route('/user_signup')
def user_signup():
    return render_template('user_signup.html')
 
@app.route('/vendor_signup')
def vendor_signup():
    return render_template('vendor_signup.html')

if __name__ == '__main__':
     app.run(debug=True)