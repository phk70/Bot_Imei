import requests

def get_services(imei, token):
    '''Получаем список доступных услуг'''
    url = f'https://imeicheck.com/api/check/{imei}'
    response = requests.get(url)  # Пол
    
    if response.status_code == 200:
        data = response.json()  # Обрабатываем ответ, по идее API возвращает json данные        
        services = [{'service_name': service['name'], 'price': service['price'], 'balance': service['balance']}
                    for service in data['services']]  # Генерируем список словарей с данными о доступных услугах
        return services
    return []

def purchase_service(imei, service_name):
    '''Оплата услуги'''
    # Аналогично здесь мы будем отправлять запрос на покупку услуги
    url = f'https://imeicheck.com/api/purchase/{imei}/{service_name}'
    response = requests.post(url)
    
    if response.status_code == 200:
        result = response.json()
        return {'success': True, 'result': result}
    return {'success': False, 'error': 'Purchase failed'}