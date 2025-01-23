import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import jwt
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Используем SQLite для простоты
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY_JWT')
db = SQLAlchemy(app)


# Модель пользователя для хранения в белом списке
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String(100), unique=True, nullable=False)

# Проверка, существует ли пользователь в белом списке
def is_user_registered(telegram_id):
    return User.query.filter_by(telegram_id=telegram_id).first() is not None

@app.route('/api/check-imei', methods=['POST'])
def check_imei():
    data = request.json
    imei = data.get('imei')
    token = data.get('token')

    # Проверка токена
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        # Проверка, зарегистрирован ли пользователь
        if not is_user_registered(payload['user']):
            return jsonify({"error": "User not registered!"}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401

    # Валидация IMEI
    if not validate_imei(imei):
        return jsonify({"error": "Invalid IMEI!"}), 400  # Если IMEI недействителен

    # Получаем список услуг
    services = get_services(imei)  # Получаем список услуг
    return jsonify(services), 200  # Возвращаем список услуг

def validate_imei(imei):
    return len(imei) == 15 and imei.isdigit()  # Проверка IMEI на наличие только 15 цифр

def get_services(imei):
    # Здесь можно добавить логику для интеграции с платными сервисами IMEI
    return [
        {"service_name": "IMEI Check Service 1", "balance": 100, "price": 10},
        {"service_name": "IMEI Check Service 2", "balance": 50, "price": 15},
    ]

# Покупка услуги
@app.route('/api/purchase', methods=['POST'])  # Маршрут для покупки услуг
def purchase_service():
    data = request.json  # Получаем данные в формате JSON
    imei = data.get('imei')  # Получаем из них IMEI
    service_name = data.get('service_name')  # И название услуги
    token = data.get('token')  # И токен

    # Проверка токена
    try:
        jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401

    # Проверка IMEI и доступных услуг
    if not validate_imei(imei):
        return jsonify({"error": "Invalid IMEI!"}), 400 

    result = purchase_imei_check(imei, service_name)
    return jsonify(result), 200

def purchase_imei_check(imei, service_name):
    # Логика для интеграции с платными сервисами
    # Здесь мы просто возвращаем фейковый результат
    return {"imei": imei, "service_name": service_name, "status": "Success", "message": "IMEI is valid!"}

# регистрация пользователей и генерация токенов
@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    telegram_id = data.get('telegram_id')

    # Проверяем, существует ли уже пользователь
    if User.query.filter_by(telegram_id=telegram_id).first() is None:
        new_user = User(telegram_id=telegram_id)
        db.session.add(new_user)
        db.session.commit()

    # Генерация токена
    token = jwt.encode({
        'user': telegram_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Срок действия 1 час
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token}), 201

if __name__ == '__main__':
    app.run(debug=True)