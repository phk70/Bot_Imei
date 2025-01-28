import requests
from flask import Flask, Response, request, jsonify


app = Flask(__name__)


@app.route('/api/check-imei', methods=['POST'])
def get_services(imei, token):
    '''Получаем список доступных услуг'''       
    data = response.get_json()  # Получаем данные из ответа
    services = [{'name': service['name'], 'price': service['price'], 'balance': service['balance']}
                for service in data['services']]  # Генерируем список словарей с данными о доступных услугах
    
    # Возвращаем список. Например список ниже
    services = [
        {'name': 'service1', 'price': 1000, 'balance': 100}, 
        {'name': 'service2', 'price': 2000, 'balance': 2000}, 
        {'name': 'service3', 'price': 3000, 'balance': 2514}
        ]    
    return services   

@app.route('/api/purchase', methods=['POST'])
def purchase_service(imei, service_name, token):
    '''Оплата услуги'''    
    response = requests.post(url)
    
    if response.status_code == 200:
        result = response.get_json()
        return {'success': True, 'result': result}
    return {'success': False, 'error': 'Purchase failed'}



