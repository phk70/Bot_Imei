from flask import Flask, Response, request, jsonify
import sqlite3
import os
import secrets

from apps import services


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


def check_imei(imei):
    '''Проверка IMEI.'''
    if len(imei) != 15 and imei is not imei.isdigit():
        return False
    return True


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()