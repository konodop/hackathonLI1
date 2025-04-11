import requests

image_path = 'qr1.jpg'

url = 'http://localhost:8080/api/upload'
place_data = {"place": "Столовая"} # можно написать вход либо выход
files = {
   'file': open(image_path, 'rb'),
   'place': (None, str(place_data))  # Отправляем place как строку
}

response = requests.post(url, files=files)

