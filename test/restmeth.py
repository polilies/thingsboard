import requests 
import json

def just_get(address, header):
    r = requests.request('GET', address, headers=header)    
    return r

def get_byid(url, op, emp_id, header):
    r = requests.request('GET', url+op+emp_id, headers=header)
    return r

def json_post(address, data, header):
    r = requests.request('POST', address, json=data, headers=header)
    return r

def put_byid(address, data, header):
    r = requests.request('PUT', address, json=data, headers=header)
    return r

def del_contents(address, header):
    r = requests.request('DELETE', address, headers=header)
    return r

def json_get(address, data, header):
    r = requests.request('GET', address, json=data, headers=header)
    return r