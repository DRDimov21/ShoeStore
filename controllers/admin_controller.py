from flask import Blueprint, request, redirect, url_for, session, render_template, flash
from services.catalog_service import catalog_service
from services.auth_service import auth_service
from services.order_service import order_service
from services.cart_service import cart_service

admin_bp = Blueprint('admin', __name__)


@admin_bp.before_request
def require_admin():
    if not session.get('is_admin'):
        return redirect(url_for('auth.login'))


@admin_bp.route('/admin')
def admin_dashboard():
    users = auth_service.get_all()
    orders = order_service.get_all()
    products = catalog_service.get_all()

    return render_template('admin/dashboard.html',
                           users=users,
                           orders=orders,
                           products=products)


@admin_bp.route('/admin/products')
def manage_products():
    products = catalog_service.get_all()
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

        product = catalog_service.add_product(name, description, color, size, price, stock)
        if product:
            flash('Продуктът е добавен успешно!')
            return redirect(url_for('admin.manage_products'))

    return render_template('admin/add_product.html')


@admin_bp.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = catalog_service.get_by_id(product_id)
    if not product:
        return "Продуктът не е намерен", 404

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        color = request.form['color']
        size = request.form['size']
        price = float(request.form['price'])
        stock = int(request.form['stock'])

        if catalog_service.update_product(product_id, name, description, color, size, price, stock):
            flash('Продуктът е обновен успешно!')
            return redirect(url_for('admin.manage_products'))

    return render_template('admin/edit_product.html', product=product)


@admin_bp.route('/admin/products/delete/<int:product_id>')
def delete_product_page(product_id):
    if catalog_service.delete_product(product_id):
        flash('Продуктът е изтрит успешно!')
    else:
        flash('Грешка при изтриване на продукта!')

    return redirect(url_for('admin.manage_products'))