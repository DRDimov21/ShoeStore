from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from services.catalog_service import catalog_service
from services.rating_service import rating_service

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

    return render_template('catalog.html', products=products, search_query=search_query,rating_service = rating_service)


@catalog_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    #Показва детайли за конкретен продукт
    product = catalog_service.get_by_id(product_id)

    if not product:
        flash('Продуктът не е намерен!')
        return redirect(url_for('catalog.view_catalog'))

    # Вземи рейтинг данни
    rating_stats = rating_service.get_rating_stats(product_id)
    ratings = rating_service.get_ratings_for_product(product_id)

    # Вземи рейтинга на текущия потребител (ако е логнат)
    user_rating = None
    if 'user_id' in session:
        user_rating = rating_service.get_user_rating_for_product(product_id, session['user_id'])

    return render_template('product_detail.html',
                           product=product,
                           rating_stats=rating_stats,
                           ratings=ratings,
                           user_rating=user_rating)

@catalog_bp.route('/product/<int:product_id>/rate', methods=['POST'])
def rate_product(product_id):
    """Добавя рейтинг и коментар за продукт"""
    if 'user_id' not in session:
        flash('Трябва да сте влезли в профила си, за да оцените продукт!')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    rating = int(request.form.get('rating'))
    comment = request.form.get('comment', '').strip()

    # Валидация
    if rating < 1 or rating > 5:
        flash('Рейтингът трябва да е между 1 и 5 звезди!')
        return redirect(url_for('catalog.product_detail', product_id=product_id))

    # Добавяне на рейтинг
    rating_service.add_rating(product_id, user_id, rating, comment)

    flash('Вашият рейтинг и коментар бяха добавени успешно!')
    return redirect(url_for('catalog.product_detail', product_id=product_id))


@catalog_bp.route('/product/<int:product_id>/ratings')
def get_product_ratings(product_id):
    """Връща всички рейтинги за продукт (за AJAX)"""
    ratings = rating_service.get_ratings_for_product(product_id)
    ratings_data = [rating.to_dict() for rating in ratings]

    return jsonify({
        'ratings': ratings_data,
        'stats': rating_service.get_rating_stats(product_id)
    })