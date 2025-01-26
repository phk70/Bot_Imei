from flask import Flask, request, jsonify
import sqlite3
import os
import secrets



app = Flask(__name__)

@app.route('/api/register', methods=['POST'])
def register():
    '''Регистрация пользователя'''
    create_db()  # Создаем базу, если она не существует    
    data = request.get_json()  # Получаем данные из api запроса
    telegram_id = data.get('telegram_id')  # Достаем telegram_id из полученных данных    
    
    if not telegram_id: 
        return jsonify({'error': 'Telegram ID обязательны.'}), 400        
    
    if check_user_exists(telegram_id):
        return jsonify({'message': f'Пользователь с telegram_id - {telegram_id} уже зарегистрирован.'}), 400    
    
    token = secrets.token_hex(16)  # Генерируем токен    
    save_user(telegram_id, token)  # И записываем в нее пользователя
    return jsonify({'message': 'Пользователь успешно зарегистрирован.'}), 200


# @app.route('/api/check-imei', methods=['POST'])
# def register():
#     data = request.get_json()
#     telegram_id = data.get('telegram_id')    
#     create_db()
#     save_user(telegram_id)
#     return jsonify({'message': 'User registered successfully'})


def check_user_exists(telegram_id):
    '''Проверка, существует ли пользователь.'''
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE telegram_id = ?', (telegram_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def permission_user_exists(telegram_id):
    '''Открывает права на пользование ботом.'''
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Проверяем, существует ли пользователь
    cursor.execute('SELECT * FROM Users WHERE telegram_id = ?', (telegram_id,))
    user = cursor.fetchone()

    if user is None:
        print("Пользователь не найден.")
    else:
        # Обновляем permission если пользователь найден
        cursor.execute('UPDATE Users SET permission = ? WHERE telegram_id = ?', (1, telegram_id))
        conn.commit()
        print("Права пользователя обновлены.")

    conn.close()


def check_admin(telegram_id):
    '''Проверка, является ли пользователь администратором.'''
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT admin FROM Users WHERE telegram_id = ?', (telegram_id,))
    admin = cursor.fetchone()
    conn.close()
    return admin


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


def save_user(telegram_id, token):
    '''Сохранение пользователя в базе данных.'''
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
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


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()