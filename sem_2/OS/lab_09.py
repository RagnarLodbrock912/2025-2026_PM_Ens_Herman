import requests
import json

url = "https://httpbin.org"

print("\n1.OPTIONS")
print("-" * 40)

response = requests.options(url + "/get")
print("Код ответа:", response.status_code)
print("Заголовки ответа:")
for key, value in response.headers.items():
    print(f"  {key}: {value}")
print("Тело ответа:", response.text if response.text else "(пусто)")

print("\n2.GET")
print("-" * 40)

params = {"name": "Иван", "lab": "9"}
print("Запрос GET:", url + "/get", "параметры:", params)

response = requests.get(url + "/get", params=params)
print("Код ответа:", response.status_code)
print("Заголовки ответа:")
for key, value in response.headers.items():
    print(f"  {key}: {value}")
print("Тело ответа:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

print("\n3.POST")
print("-" * 40)

data = {"student": "Петров", "lab": "9", "score": 100}
print("Запрос POST:", url + "/post")
print("Данные:", json.dumps(data, ensure_ascii=False))

response = requests.post(url + "/post", json=data)
print("Код ответа:", response.status_code)
print("Заголовки ответа:")
for key, value in response.headers.items():
    print(f"  {key}: {value}")
print("Тело ответа:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
