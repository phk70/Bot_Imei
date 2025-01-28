from flask import Flask, Response, request, jsonify
import sqlite3
import os
import secrets


# 5285926615
app = Flask(__name__)


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


@app.route('/api/register', methods=['POST'])
def register():
    '''Регистрация пользователя'''    
    data = request.get_json()  # Получаем данные из api запроса
    telegram_id = data.get('telegram_id')  # Достаем telegram_id из полученных данных   
    token = data.get('token')  # И token
    if not telegram_id or not token: 
        return jsonify({'error': 'Telegram ID  и Token обязательны.'}), 400    
    if check_user_exists(telegram_id):
        return jsonify({'message': f'Пользователь с telegram_id - {telegram_id} уже зарегистрирован.'}), 400    
    return jsonify({'message': 'Пользователь успешно зарегистрирован.'}), 200


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


def check_user_exists(telegram_id):
    '''Проверка, существует ли пользователь.'''
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE telegram_id = ?', (telegram_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def validate_imei(imei):
    '''Проверка IMEI.'''
    if len(imei) != 15 and imei is not imei.isdigit():
        return False
    return True


def open_permission_user(telegram_id):
    '''Открывает права на пользование ботом.'''
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()    
    cursor.execute('SELECT * FROM Users WHERE telegram_id = ?', (telegram_id,))
    user = cursor.fetchone()  # Проверяем, существует ли пользователь
    if user is None:
        print('Пользователь не найден.')
        return False
    else:        
        cursor.execute('UPDATE Users SET permission = ? WHERE telegram_id = ?', (1, telegram_id))  # Обновляем permission если пользователь найден
        conn.commit()
        print('Права пользователя обновлены.')
    conn.close()
    return True


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
    


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()