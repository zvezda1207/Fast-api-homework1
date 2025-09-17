import requests

# data = requests.post('http://127.0.0.1:8000/api/v1/adv', json={
# 'title': 'IPhone',
# 'description': 'Phone',
# 'price': 150.0,
# 'author': 'John Doe'
# })
# print (data.status_code)
# print (data.json())

data = requests.post('http://127.0.0.1:8000/api/v1/adv', json={
"title": "Test 1 Docker",
"description": "Testing API in container",
"price": 250,
"author": "User"})
print (data.status_code)
print (data.json())



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

# response = requests.get('http://127.0.0.1:8000/api/v1/adv', 
#                        params={
#                            'price_from': 100,
#                            'price_to': 500
#                        })
# print("\nSearch by price range:")
# print(response.status_code)
# print(response.json())



