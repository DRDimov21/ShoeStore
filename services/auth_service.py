users = []
next_user_id = 1


def register_user(email, password, name):
    global next_user_id


    if any(user['email'] == email for user in users):
        return None

    user = {
        'id': next_user_id,
        'email': email,
        'password': password,
        'name': name,
        'is_admin': False
    }

    users.append(user)
    next_user_id += 1
    return user


def login_user(email, password):
    user = next((user for user in users if user['email'] == email and user['password'] == password), None)
    return user


def get_user_by_id(user_id):
    return next((user for user in users if user['id'] == user_id), None)


def get_all_users():
    return users



def create_default_admin():
    global next_user_id
    admin_user = {
        'id': next_user_id,
        'email': 'admin@shoestore.com',
        'password': 'admin123',
        'name': 'admin',
        'is_admin': True
    }
    users.append(admin_user)
    next_user_id += 1



create_default_admin()