from flask import Blueprint, request, redirect, url_for, session, render_template, flash
from services.catalog_service import add_product, update_product, delete_product, get_product_by_id
from services.auth_service import get_all_users
from services.order_service import get_all_orders

admin_bp = Blueprint('admin', __name__)


@admin_bp.before_request
def require_admin():
    if not session.get('is_admin'):
        return redirect(url_for('auth.login'))


@admin_bp.route('/admin')
def admin_dashboard():
    users = get_all_users()
    orders = get_all_orders()
    from services.catalog_service import get_all_products
    products = get_all_products()

    return render_template('admin/dashboard.html',
                           users=users,
                           orders=orders,
                           products=products)


@admin_bp.route('/admin/products')
def manage_products():
    from services.catalog_service import get_all_products
    products = get_all_products()
    return render_template('admin/products.html', products=products)


@admin_bp.route('/admin/products/add', methods=['GET', 'POST'])
def add_product_page():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        color = request.form['color']
        size = request.form['size']
        price = float(request.form['price'])
        stock = int(request.form['stock'])

        product = add_product(name, description, color, size, price, stock)
        if product:
            flash('Продуктът е добавен успешно!')
            return redirect(url_for('admin.manage_products'))

    return render_template('admin/add_product.html')


@admin_bp.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return "Продуктът не е намерен", 404

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        color = request.form['color']
        size = request.form['size']
        price = float(request.form['price'])
        stock = int(request.form['stock'])

        if update_product(product_id, name, description, color, size, price, stock):
            flash('Продуктът е обновен успешно!')
            return redirect(url_for('admin.manage_products'))

    return render_template('admin/edit_product.html', product=product)


@admin_bp.route('/admin/products/delete/<int:product_id>')
def delete_product_page(product_id):
    if delete_product(product_id):
        flash('Продуктът е изтрит успешно!')
    else:
        flash('Грешка при изтриване на продукта!')

    return redirect(url_for('admin.manage_products'))