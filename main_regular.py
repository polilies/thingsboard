from http import client
from operator import index
from pydoc import cli
from time import sleep
from pydantic import BaseModel, validator
import json
from typing import List, Optional
#import requests
from restmeth import *
from mod_funcs import *
import datetime as t
import time

url1 = 'http://10.46.1.193:8080/api/v1/'
url2 = '/telemetry'
minutes =[0,10,20,30,40,50]

#test_data = {"temperature": 189.4, "humid":23.2}
headers = {'Content-Type':'application/json'}
index_reg = [0,1,2,3,4,5,6,7,8,13,17,21,25,34,38,50,54]
keys= ["Van","Vbn","Vcn","Vab","Vbc","Vca","Ia","Ib","Ic","P","S","Q","F","Wcon","Wdel","Qend","Qcap"]



class Model(BaseModel):
    feeder_name: Optional[str]
    ip: str
    port: int
    mod_address: int
    dev_token : str
    reg_list: int
    count: int
    reg_type: str
    
def post_device_data(address, data, header):
    resp = json_post(address=address,data=data, header=header)
    return resp

def read_conf():
    path = 'dev_conf.json'
    with open(path) as f:
        data = json.load(f)
    device_list: List[Model] = [Model(**item) for a in data for item in data[a]]
    return device_list
    
#reads modbus device data and returns a dictionary of the read values
def read_dev(ip, port, dev_add, cnt,reg):
    client = tcp_modbus(ip,port)
    i = read_holding_float(reg=reg,cnt=cnt,d_address= dev_add, remote= client)
    client.close()
    return i

def dicter(data, keys, indexes):
    print(len(data),len(keys), len(indexes))
    filtered_data =[data[i] for i in indexes]
    last_dict = {keys[i]: filtered_data[i] for i in range(len(indexes))}
    return last_dict    

def get_minute():
    return t.datetime.now().minute

def main() -> None:
    dev = read_conf()
    #print(url1 + dev[0].dev_token + url2)
    let = True
    while True:
        if (get_minute() in minutes) and let:
            raw_data = read_dev(dev[0].ip,dev[0].port,dev[0].mod_address, dev[0].count,dev[0].reg_list)
            data = dicter(raw_data,keys=keys, indexes=index_reg)   
            resp = post_device_data(url1 + dev[0].dev_token + url2, data, headers)  
            #print(resp)
            let = False
        elif get_minute not in minutes:
            let = True
        
        time.sleep(30)
        
    
if __name__ == '__main__':
    main()