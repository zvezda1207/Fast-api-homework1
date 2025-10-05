import requests

# data = requests.post('http://127.0.0.1:8000/api/v1/adv', json={
# 'title': 'IPhone',
# 'description': 'Phone',
# 'price': 150.0,
# 'author': 'John Doe'
# })
# print (data.status_code)
# print (data.json())

# data = requests.post('http://127.0.0.1:8000/api/v1/adv', json={
# "title": "Test 1 Docker",
# "description": "Testing API in container",
# "price": 250,
# "author": "User"})
# print (data.status_code)
# print (data.json())



# data = requests.get('http://127.0.0.1:8000/api/v1/adv/10')
# print (data.status_code)
# print (data.json())

# data = requests.patch('http://127.0.0.1:8000/api/v1/adv/10', json={'title': 'New phone'})
# print (data.status_code)
# print (data.json())

# data = requests.delete('http://127.0.0.1:8000/api/v1/adv/10')
# print (data.status_code)
# print (data.json())

# data = requests.get('http://127.0.0.1:8000/api/v1/adv/', params={'author': 'John Doe'})
# print("\nSearch by author:")
# print (data.status_code)
# print (data.json())



data = requests.post('http://127.0.0.1:8000/api/v1/user', json={'name': 'admin1', 'password': '1234'})
print(data.status_code)
print(data.text)
print(data.json())

data = requests.post('http://127.0.0.1:8000/api/v1/user/login', json={'name': 'admin1', 'password': '1234'})
print(data.status_code)
print(data.json())
token = data.json()['token']

data = requests.post('http://127.0.0.1:8000/api/v1/adv', json={'title': 'adv_1', 'description': 'Testing',
'price': 250, 'author': 'admin1'}, headers={'x-token': token})
print(data.status_code)
if data.status_code == 200:
    print(data.json())
else:
    print("Ошибка:", data.text) 


# data = requests.get('http://127.0.0.1:8000/api/v1/adv/3', headers={'x-token': token})
# print(data.status_code)
# print(data.json())



