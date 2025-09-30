from flask import Blueprint, request, redirect, url_for, session, render_template, flash
from services.auth_service import register_user, login_user, get_user_by_id

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']

        user = register_user(email, password, name)
        if user:
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['is_admin'] = user.get('is_admin', False)
            print(f"✅ Регистриран нов потребител: {email}")
            '''return redirect(url_for('catalog.view_catalog'))'''
        else:
            flash('Вече има регистриран потребител с този email!')

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = login_user(email, password)
        if user:
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['is_admin'] = user.get('is_admin', False)
            '''return redirect(url_for('catalog.view_catalog'))'''
        else:
            flash('Грешен email или парола!')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))