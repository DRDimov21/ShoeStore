from flask import Flask, render_template, session
from controllers.auth_controller import auth_bp
from controllers.catalog_controller import catalog_bp
from controllers.cart_controller import cart_bp
from controllers.admin_controller import admin_bp


from services.cart_service import cart_service
from services.catalog_service import catalog_service
from services.order_service import order_service

app = Flask(__name__)
app.secret_key = 'shoestore_secret_key'


order_service.set_services(cart_service, catalog_service)


app.register_blueprint(auth_bp)
app.register_blueprint(catalog_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)