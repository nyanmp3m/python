#!/usr/bin/env venv/bin/python

import requests

master_url = "http://localhost:5000"
slave1_url = "http://localhost:5001"
slave2_url = "http://127.0.0.1:5002"


def check():
    print(requests.get(f'{master_url}/products').json())
    print(requests.get(f'{slave1_url}/products').json())
    print(requests.get(f'{slave2_url}/products').json())

print(requests.post(f'{master_url}/products', json={"name": "labubu"}).json())
print(requests.post(f'{master_url}/sync').json())

check()

print(requests.post(f'{slave2_url}/products', json={"name": "labubu"}).json())

check()

products = requests.get(f'{master_url}/products').json().get('products')
print(requests.post(f'{slave2_url}/replicate', json={"products": products}))

check()