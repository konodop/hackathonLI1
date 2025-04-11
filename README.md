<h2>Как делать запросы<h2\><h4>
<div class="highlight highlight-source-shell notranslate position-relative overflow-auto" dir="auto"><pre>import requests

# URL вашего API
url = "http://localhost:8080/api/teacher/sign-up"

# Данные для регистрации
sign_up_request = {
    "name": "ХЗ",
    "surname": "Абый",
    "fathername": "Додепович",
    "login": "john@example.com",
    "password": "12345678",
    "subject": "Урок"
}

# Отправка POST-запроса
response = requests.post(url, json=sign_up_request)

# Проверка ответа
if response.status_code == 200:
    print("Регистрация прошла успешно:", response.json())
else:
    print("Ошибка при регистрации:", response.status_code, response.text)
</pre></div><\h4>
