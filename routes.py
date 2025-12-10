from flask import render_template, request, redirect, url_for, session, flash, jsonify
from app import app, db
from models import Category, MenuItem, Order, OrderItem
import json
import os
from functools import wraps
from datetime import datetime

# --- SECURITY HELPER ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Please log in to access the admin panel.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# --- EMAIL SIMULATION HELPER ---
def send_order_notification(order, status):
    """
    Simulates sending an email by printing to the terminal.
    This avoids needing real email/password verification for now.
    """
    subject = ""
    body = ""
    
    if status == 'cancelled':
        subject = f"Update on Order #{order.id}: Cancelled"
        body = f"Dear {order.customer_name},\n\nWe regret to inform you that your order #{order.id} has been cancelled.\n\nIf you have questions, please contact us."
    elif status == 'confirmed':
        subject = f"Order #{order.id} Confirmed!"
        body = f"Dear {order.customer_name},\n\nGreat news! Your order #{order.id} has been accepted and is being prepared."
    elif status == 'out_for_delivery':
        subject = f"Order #{order.id} is on the way!"
        body = f"Dear {order.customer_name},\n\nYour food is out for delivery. Get your plates ready!"
    elif status == 'delivered':
        subject = f"Order #{order.id} Delivered"
        body = f"Dear {order.customer_name},\n\nEnjoy your meal! Thank you for ordering with FoodHub."

    # --- SIMULATION: PRINT TO TERMINAL ---
    print("\n" + "="*50)
    print(f" [EMAIL SENT AUTOMATICALLY]")
    print(f" To: {order.customer_email}")
    print(f" Subject: {subject}")
    print(f" Body: {body}")
    print("="*50 + "\n")

# --- PUBLIC ROUTES ---

@app.route('/')
def index():
    categories = Category.query.all()
    popular_items = MenuItem.query.filter_by(is_popular=True, is_available=True).limit(6).all()
    return render_template('index.html', categories=categories, popular_items=popular_items)


@app.route('/menu')
def menu():
    category_id = request.args.get('category', type=int)
    categories = Category.query.all()
    
    if category_id:
        items = MenuItem.query.filter_by(category_id=category_id, is_available=True).all()
        current_category = Category.query.get(category_id)
    else:
        items = MenuItem.query.filter_by(is_available=True).all()
        current_category = None
    
    return render_template('menu.html', categories=categories, items=items, current_category=current_category)


@app.route('/cart')
def cart():
    cart_items = get_cart_items()
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    delivery_fee = 2.99 if cart_items else 0
    total = subtotal + delivery_fee
    return render_template('cart.html', cart_items=cart_items, subtotal=subtotal, 
                         delivery_fee=delivery_fee, total=total)


@app.route('/add-to-cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    item = MenuItem.query.get_or_404(item_id)
    cart = session.get('cart', {})
    
    item_key = str(item_id)
    if item_key in cart:
        cart[item_key]['quantity'] += 1
    else:
        cart[item_key] = {
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'image_url': item.image_url,
            'quantity': 1
        }
    
    session['cart'] = cart
    flash(f'{item.name} added to cart!', 'success')
    
    referrer = request.referrer
    if referrer:
        return redirect(referrer)
    return redirect(url_for('menu'))


@app.route('/update-cart/<int:item_id>', methods=['POST'])
def update_cart(item_id):
    action = request.form.get('action')
    cart = session.get('cart', {})
    item_key = str(item_id)
    
    if item_key in cart:
        if action == 'increase':
            cart[item_key]['quantity'] += 1
        elif action == 'decrease':
            cart[item_key]['quantity'] -= 1
            if cart[item_key]['quantity'] <= 0:
                del cart[item_key]
        elif action == 'remove':
            del cart[item_key]
    
    session['cart'] = cart
    return redirect(url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = get_cart_items()
    if not cart_items:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('menu'))
    
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    delivery_fee = 2.99
    total = subtotal + delivery_fee
    
    if request.method == 'POST':
        order = Order(
            customer_name=request.form['name'],
            customer_email=request.form['email'],
            customer_phone=request.form['phone'],
            delivery_address=request.form['address'],
            delivery_instructions=request.form.get('instructions', ''),
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total=total,
            status='pending'  # Initial status is pending
        )
        db.session.add(order)
        db.session.flush()
        
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=item['id'],
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)
        
        db.session.commit()
        session['cart'] = {}
        
        # Send initial received email
        send_order_notification(order, 'received')
        
        return redirect(url_for('order_confirmation', order_id=order.id))
    
    return render_template('checkout.html', cart_items=cart_items, subtotal=subtotal,
                         delivery_fee=delivery_fee, total=total)


@app.route('/order-confirmation/<int:order_id>')
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_confirmation.html', order=order)


@app.route('/track-order', methods=['GET', 'POST'])
def track_order():
    order = None
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        email = request.form.get('email')
        order = Order.query.filter_by(id=order_id, customer_email=email).first()
        if not order:
            flash('Order not found. Please check your order ID and email.', 'error')
    return render_template('track_order.html', order=order)


@app.route('/orders')
def order_history():
    orders = Order.query.order_by(Order.created_at.desc()).limit(20).all()
    return render_template('order_history.html', orders=orders)


# --- ADMIN AUTHENTICATION ---

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        valid_user = os.environ.get("ADMIN_USERNAME", "admin")
        valid_pass = os.environ.get("ADMIN_PASSWORD", "ashish123")
        
        if username == valid_user and password == valid_pass: 
            session['is_admin'] = True
            flash('Welcome back, Admin!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials.', 'error')
            
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))


# --- ADMIN ROUTES (PROTECTED) ---

@app.route('/admin')
@admin_required
def admin():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    items = MenuItem.query.all()
    categories = Category.query.all()
    
    pending_count = Order.query.filter_by(status='pending').count()
    confirmed_count = Order.query.filter_by(status='confirmed').count()
    today_orders = Order.query.filter(
        db.func.date(Order.created_at) == db.func.current_date()
    ).all()
    today_revenue = sum(o.total for o in today_orders)
    
    return render_template('admin.html', orders=orders, items=items, categories=categories,
                         pending_count=pending_count, confirmed_count=confirmed_count,
                         today_revenue=today_revenue)


@app.route('/admin/order/<int:order_id>/update-status', methods=['POST'])
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    # Update Database
    order.status = new_status
    db.session.commit()
    
    # Send Automatic Email (Simulated)
    send_order_notification(order, new_status)
    
    # Custom Messages for the Admin
    if new_status == 'cancelled':
        flash(f'Message is canceled. Automatic notification sent to {order.customer_email}.', 'error')
    elif new_status == 'confirmed':
        flash(f'Order Accepted! Automatic notification sent to {order.customer_email}.', 'success')
    else:
        flash(f'Order status updated to {new_status}.', 'success')
        
    return redirect(url_for('admin'))


@app.route('/admin/order/<int:order_id>/delete', methods=['POST'])
@admin_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash(f'Order #{order_id} has been deleted.', 'success')
    return redirect(url_for('admin'))


@app.route('/admin/menu/add', methods=['POST'])
@admin_required
def add_menu_item():
    item = MenuItem(
        name=request.form['name'],
        description=request.form['description'],
        price=float(request.form['price']),
        category_id=int(request.form['category_id']),
        image_url=request.form.get('image_url', ''),
        is_available=True,
        is_popular='is_popular' in request.form
    )
    db.session.add(item)
    db.session.commit()
    flash(f'{item.name} added to menu!', 'success')
    return redirect(url_for('admin'))


@app.route('/admin/menu/<int:item_id>/delete', methods=['POST'])
@admin_required
def delete_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f'{item.name} removed from menu!', 'success')
    return redirect(url_for('admin'))


@app.route('/admin/menu/<int:item_id>/toggle', methods=['POST'])
@admin_required
def toggle_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    item.is_available = not item.is_available
    db.session.commit()
    status = 'available' if item.is_available else 'unavailable'
    flash(f'{item.name} is now {status}!', 'success')
    return redirect(url_for('admin'))


@app.route('/admin/category/add', methods=['POST'])
@admin_required
def add_category():
    category = Category(
        name=request.form['name'],
        icon=request.form.get('icon', 'fa-utensils')
    )
    db.session.add(category)
    db.session.commit()
    flash(f'Category {category.name} added!', 'success')
    return redirect(url_for('admin'))


@app.route('/admin/category/<int:category_id>/delete', methods=['POST'])
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.items:
        flash(f'Cannot delete "{category.name}" because it still has menu items. Please delete the food items first.', 'error')
        return redirect(url_for('admin'))
        
    db.session.delete(category)
    db.session.commit()
    flash(f'Category "{category.name}" deleted successfully!', 'success')
    return redirect(url_for('admin'))


# --- HELPERS ---

def get_cart_items():
    cart = session.get('cart', {})
    return list(cart.values())


@app.context_processor
def cart_count():
    cart = session.get('cart', {})
    count = sum(item['quantity'] for item in cart.values())
    return {'cart_count': count}