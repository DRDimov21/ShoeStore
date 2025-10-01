from flask import Blueprint, request, redirect, url_for, session, render_template, flash
from services.auth_service import auth_service

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']

        user = auth_service.register_user(email, password, name)
        if user:
            print(f"✅ Регистриран нов потребител: {email}")
            flash('Регистрацията е успешна! Моля, влезте в профила си.')
            return redirect(url_for('auth.login'))
        else:
            flash('Вече има регистриран потребител с този email!')

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = auth_service.login_user(email, password)
        if user:
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_name'] = user.name
            session['is_admin'] = user.is_admin
            return redirect(url_for('catalog.view_catalog'))
        else:
            flash('Грешен email или парола!')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))