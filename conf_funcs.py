#https://jsontopydantic.com/   otomatik olarak pydantic modeli cikarmakta.

from pydantic import BaseModel, validator
import json
import pydantic
from restmeth import *
from typing import List, Optional
import datetime as t
import logging

'''
class RegInfoItem(BaseModel):
    start_reg: int
    count: int
    index: List[int]
    keys: List[str]
    scales: List[float]
    typo: str
'''
class Device(BaseModel):
    dev_name: Optional[str]
    ip: str
    port: int
    dev_type: str
    mod_adrs: int
    dev_token : str
    #reg_info: List[RegInfoItem]
    
class Model(BaseModel):
    devices: List[Device]  
    
    
def post_device_data(address, data, header):
    resp = json_post(address=address,data=data, header=header)
    return resp

def read_conf():
    path = '.\conf_files\dev_conf.json'
    with open(path) as f:
        data = json.load(f)
    print(type(data))
    device_list: List[Model] = [Model(**item) for a in data for item in data[a]]
    return device_list

'''
read_conf_sep() fonksiyonu cihaz kayıtları ile cihaz register kayitlarini ayri okumayi amaclamakta,
boylelikle web sayfasindan register kayitlari birden fazla cihazin bulundugu durumlarda tekrar tekrar
girilme ihtiyaci duyulmayacak. Yalnizca ip ya da modbus adress gibi her cihazda degisebilen degerler girilmesi
zaruri olacak
'''
def read_conf_sep():
    path_dev = '.\conf_files\dev_conf.json'
    path_reg = '.\conf_files\\reg_conf.json'
    with open(path_dev) as f:
        dev_data = json.load(f)
    with open(path_reg) as a:
        reg_data = json.load(a)
    
    
         
    
    #print(type(dev_data))
    #print(f"{reg_data['umg605']}")
    device_list: List[Device] = [Device(**item) for a in dev_data for item in dev_data[a]]
    #return device_list
    return device_list, reg_data




def dicter(data, keys, indexes, scales):
    print(len(data),len(keys), len(indexes))
    if len(data) >= indexes[-1] + 1: #chechking that modbus fetched data lenght longer than last index point!
        indexed_data =[data[i] for i in indexes]
        scaled = [indexed_data[i]*scales[i] for i in range(len(scales))]
        last_dict = {keys[i]: scaled[i] for i in range(len(indexes))}
        return last_dict
    else:
        print("provided data lenght is longer than last index number")

def get_minute():
    return t.datetime.now().minute