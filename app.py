from flask import Flask, request, jsonify
import sqlite3
import os
import secrets


app = Flask(__name__)


# {"telegram_id": "454646", "token":"11111111"}  # Для проверки

@app.route('/api/register', methods=['POST'])
def register():
    '''Регистрация пользователя'''  
    response = request.get_json()       
    telegram_id = response.get('telegram_id')
    token = response.get('token')

    if not telegram_id or not token: 
        return jsonify({'error': 'Telegram ID  и Token обязательны.'}), 400    
    
    return jsonify({'message': 'Пользователь успешно зарегистрирован.'}), 200


# {"imei": "123456789123456", "token":"123456"}  # Для проверки

@app.route('/api/check-imei', methods=['POST'])
def get_services():
    '''Получаем список доступных услуг'''       
    response = request.get_json()
    imei = response.get('imei')
    token = response.get('token')
    
    if not imei or not token:
        return jsonify({'error': 'IMEI и Token обязательны'}), 400
    
    if not check_imei(imei):
        return jsonify({'error': 'Не корректный IMEI'}), 400
    
    services = [
        {'name': 'service1', 'price': 1000, 'balance': 100}, 
        {'name': 'service2', 'price': 2000, 'balance': 2000}, 
        {'name': 'service3', 'price': 3000, 'balance': 2514}
        ]        

    return services, 200   


# {"imei": "12365255", "service_name": "IMEI Checker", "token": "123123123"}  # Для проверки

@app.route('/api/purchase', methods=['POST'])
def service_purchase():
    response = request.get_json()
    imei = response.get('imei')
    service_name = response.get('service_name')
    token = response.get('token')

    if not imei or not service_name or not token:
        return jsonify({'error': 'IMEI, Service_name и Token обязательны'}), 400
    
    if not check_imei(imei):
        return jsonify({'error': 'Не корректный IMEI'}), 400

    check_result = [{'service_name': service_name, 'check_result': 'Ваш телефон серее серого'}]

    return check_result, 200


def validate_imei(imei):
    '''Проверка IMEI.'''
    if len(imei) != 15 and imei is not imei.isdigit():
        return False
    return True


def create_db():
    '''Создание базы данных.'''
    if not os.path.exists('users.db'):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()  
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        telegram_id TEXT NOT NULL,
        token TEXT NOT NULL,
        admin BOOLEAN DEFAULT FALSE,
        permission BOOLEAN DEFAULT FALSE
        )
        ''')  
        conn.commit()
        conn.close()


def save_user(telegram_id):
    '''Сохранение пользователя в базе данных.'''
    if not os.path.exists('users.db'):
        create_db()

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    token = secrets.token_hex(16)  # Генерируем токен
    cursor.execute('INSERT INTO Users (telegram_id, token, admin, permission) VALUES (?, ?, ?, ?)', (telegram_id, token, False, False))
    conn.commit()
    conn.close()


def delete_user(telegram_id):
    '''Удаление пользователя из базы данных.'''
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Users WHERE telegram_id = ?', (telegram_id,))
    conn.commit()
    conn.close() 


def get_all_permissions_for_admin(telegram_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()    
    cursor.execute('SELECT * FROM Users WHERE telegram_id = ?', (telegram_id,))
    user = cursor.fetchone()  # Выбираем пользователя
    if user is None:
        print('Пользователь не найден.')
        return False
    else:        
        cursor.execute('UPDATE Users SET permission = ? WHERE telegram_id = ?', (1, telegram_id))  # Обновляем permission если пользователь найден
        cursor.execute('UPDATE Users SET admin = ? WHERE telegram_id = ?', (1, telegram_id))
        conn.commit()
        print('Права пользователя {telegram_id} обновлены.')
    conn.close()


def check_admin(telegram_id):
    '''Проверка, является ли пользователь администратором.'''
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT admin FROM Users WHERE telegram_id = ?', (telegram_id,))
    admin = cursor.fetchone()
    conn.close()  
    if admin[0] == 0:
        return False  
    else:
        return True


def check_user_permission(telegram_id):
    '''Проверка, имеет ли пользователь доступ к боту.'''
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT permission FROM Users WHERE telegram_id = ?', (telegram_id,))
    permission = cursor.fetchone()
    conn.close()  
    if permission[0] == 0:
        return False  
    else:
        return True


def open_permission_user(telegram_id):
    '''Открывает права на пользование ботом.'''
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()    
    cursor.execute('SELECT * FROM Users WHERE telegram_id = ?', (telegram_id,))
    user = cursor.fetchone()    # Выбираем пользователя
    if user is None:
        print('Пользователь не найден.')
        return False
    else:        
        cursor.execute('UPDATE Users SET permission = ? WHERE telegram_id = ?', (1, telegram_id))  # Обновляем permission если пользователь найден
        conn.commit()
        print('Права пользователя обновлены.')
    conn.close()
    return True


def check_user_exists(telegram_id):
    '''Проверка, существует ли пользователь.'''
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE telegram_id = ?', (telegram_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()