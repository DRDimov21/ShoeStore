from flask import Blueprint, request, redirect, url_for, session, render_template, flash
from services.catalog_service import catalog_service
from services.order_service import order_service
from services.cart_service import cart_service
cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/cart')
def view_cart():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    cart = cart_service.get_cart(user_id)
    total = sum(item['product']['price'] * item['quantity'] for item in cart)

    return render_template('cart.html', cart=cart, total=total)


@cart_bp.route('/cart/add/<int:product_id>', methods=['POST'])
def add_product_to_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    quantity = int(request.form.get('quantity', 1))
    size = request.form.get('size')


    if cart_service.add_to_cart(user_id, product_id, quantity):
        flash('Продуктът е добавен в кошницата!')
    else:
        flash('Грешка при добавяне на продукта!')

    return redirect(url_for('catalog.view_catalog'))


@cart_bp.route('/cart/remove/<int:product_id>')
def remove_product_from_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    cart_service.remove_from_cart(user_id, product_id)
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    cart = cart_service.get_cart(user_id)

    if not cart:
        flash('Кошницата е празна!')
        return redirect(url_for('cart.view_cart'))

    if request.method == 'POST':
        address = request.form['address']
        payment_method = request.form['payment_method']

        order = order_service.create_order(user_id, address, payment_method)
        if order:
            cart_service.clear_cart(user_id)
            flash(f'Поръчката е направена успешно! Номер на поръчка: {order.id}')
            return redirect(url_for('catalog.view_catalog'))
        else:
            flash('Грешка при създаване на поръчката!')

    total = sum(item['product']['price'] * item['quantity'] for item in cart)
    return render_template('checkout.html', cart=cart, total=total)