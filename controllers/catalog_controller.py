from flask import Blueprint, render_template, request, session
from services.catalog_service import catalog_service

catalog_bp = Blueprint('catalog', __name__)


@catalog_bp.route('/catalog')
def view_catalog():
    products = catalog_service.get_all()


    search_query = request.args.get('search', '')
    if search_query:
        products = catalog_service.search_products(search_query)


    color_filter = request.args.get('color', '')
    size_filter = request.args.get('size', '')
    max_price = request.args.get('max_price', '')

    if color_filter or size_filter or max_price:
        products = catalog_service.filter_products(products, color_filter, size_filter, max_price)

    return render_template('catalog.html', products=products, search_query=search_query)


@catalog_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = catalog_service.get_by_id(product_id)
    if product:
        return render_template('product_detail.html', product=product)
    return "Продуктът не е намерен", 404