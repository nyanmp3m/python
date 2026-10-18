import random
import requests
from flask import Flask, render_template_string
from flask import request

app = Flask(__name__)

SERVERS = [
    'http://localhost:5001',  # firstServer.py
    'http://localhost:5002',  # secondServer.py
    'http://localhost:5003',  # thirdServer.py
]

# Сделано нейронкой для удобства)))))
PAGE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Клиент</title>
</head>
<body>
    <h1>{{ title }}</h1>
    <p><strong>Ответ:</strong> {{ result }}</p>
    <p><em>Сервер: {{ server }}</em></p>

</body>
</html>
'''


@app.route('/')
def index():
    server = random.choice(SERVERS)
    try:
        if server.split(':')[-1] == '5003':
            resp = requests.post(f'{server}/generate-random-chars', json={'count': 5}, timeout=3)
        elif server.split(':')[-1] == '5002':
            resp = requests.get(f'{server}/get-random-nums', timeout=3)
        else:
            resp = requests.get(f'{server}/get-current-time', timeout=3)
        data = resp.json()

        title = ''
        if 'current_time' in data:
            result = data['current_time']
            server = server
            title = 'Текущее время'
        elif 'numbers' in data:
            result = ', '.join(map(str, data['numbers']))
            server = server
            title = 'Случайные числа'
        elif 'chars' in data:
            result = ', '.join(data['chars'])
            server = server
            title = 'Случайные символы'
        else:
            result = data.get('error', 'нет данных')
            server = server
            title = 'Ошибка'


        return render_template_string(
            PAGE,
            title=title,
            result=result,
            server=server
        )
        
    except Exception as e:
        time_result = f'Ошибка: {e}'
        time_server = server


if __name__ == '__main__':
    app.run(debug=True)