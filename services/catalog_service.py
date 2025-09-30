# Данни в паметта
products = []
next_product_id = 1


def get_all_products():
    return [p for p in products if p['stock'] > 0]


def get_product_by_id(product_id):
    return next((p for p in products if p['id'] == product_id), None)


def add_product(name, description, color, size, price, stock):
    global next_product_id

    product = {
        'id': next_product_id,
        'name': name,
        'description': description,
        'color': color,
        'size': size,
        'price': price,
        'stock': stock
    }

    products.append(product)
    next_product_id += 1
    return product


def update_product(product_id, name, description, color, size, price, stock):
    product = get_product_by_id(product_id)
    if product:
        product.update({
            'name': name,
            'description': description,
            'color': color,
            'size': size,
            'price': price,
            'stock': stock
        })
        return True
    return False


def delete_product(product_id):
    global products
    products = [p for p in products if p['id'] != product_id]
    return True


def search_products(query):
    query = query.lower()
    return [p for p in products if
            query in p['name'].lower() or
            query in p['color'].lower() or
            query in p['description'].lower()]


def filter_products(products_list, color, size, max_price):
    filtered = products_list

    if color:
        filtered = [p for p in filtered if p['color'].lower() == color.lower()]

    if size:
        filtered = [p for p in filtered if p['size'] == size]

    if max_price:
        filtered = [p for p in filtered if p['price'] <= float(max_price)]

    return filtered


def decrease_stock(product_id, quantity):
    product = get_product_by_id(product_id)
    if product and product['stock'] >= quantity:
        product['stock'] -= quantity
        return True
    return False


# Инициализация с примерни продукти
def initialize_sample_products():
    global next_product_id
    sample_products = [
        {
            'id': next_product_id, 'name': 'Nike Air Max', 'description': 'Спортни обувки за всеки ден',
            'color': 'черни', 'size': '42', 'price': 199.99, 'stock': 10
        },
        {
            'id': next_product_id + 1, 'name': 'Adidas Ultraboost', 'description': 'Обувки за бягане',
            'color': 'бели', 'size': '43', 'price': 229.99, 'stock': 8
        },
        {
            'id': next_product_id + 2, 'name': 'Vans Old Skool', 'description': 'Класически кецове',
            'color': 'черно-бели', 'size': '41', 'price': 89.99, 'stock': 15
        }
    ]

    products.extend(sample_products)
    next_product_id += 3


initialize_sample_products()