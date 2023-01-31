from dataclasses import dataclass
from operator import index
from typing import List, Optional, Dict
from mod_funcs_exc import *
from pymodbus import exceptions as mb_ex
from restmeth import * 
import json
from datetime import datetime as t
import time
import socket
'''
@dataclass
class RegData:
'''    

func_dict = {"holding_float": read_holding_float, "holding_S32": read_holding_S32,
             "holding_S16": read_holding_S16, "input_S16": read_input_S16,
             "input_RS32": read_input_RS32, "input_Rfloat": read_input_floatRwords}

server = socket.gethostbyname('alican_mytb_1') # getting ip of the thingsboard  
url1 = 'http://' + server + ':9090/api/v1/' #this is the docker network ip address, logger also in the same location
#url1 = 'http://172.24.0.3/api/v1/' #this is the docker network ip address, logger also in the same location
url2 = '/telemetry'
headers = {'Content-Type':'application/json'}
minutes =[0,10,20,30,40,50]

@dataclass
class RegInfoItem:
    start_reg: int
    count: int
    index: List[int]
    keys: List[str]
    scales: List[float]
    typo: str

@dataclass
class Device:
    dev_name: Optional[str]
    ip: str
    port: int
    dev_type: str
    mod_adrs: int
    dev_token : str
    reg_info: List[RegInfoItem]
    

def read_conf_sep():
    path_dev = './conf_files/dev_conf.json' #this must be like '..\.\conf_files\dev_conf.json'  in the windows machines 
    path_reg = './conf_files/reg_conf.json' # '..\.\conf_files\reg_conf.json'
    with open(path_dev) as f:
        dev_data = json.load(f)
    with open(path_reg) as a:
        reg_data = json.load(a)
    
    device_list: List[Device] = [Device(**item) for a in dev_data for item in dev_data[a]]
    unique_devs = set([dev.dev_type for dev in device_list]) # if there is more then one same kind
    
    #for the connections. There must be unique connections
    unique_ips = list(set([dev.ip for dev in device_list]))               
    #print(unique_ips)
    #unique_ips = list(map(dict, set(tuple(sorted(d.items())) for d in unique_ips.items())))
    dev_indexes = list()
    for ip in unique_ips:
        dev_indexes.append([device_list.index(a) for a in device_list if ip == a.ip])
    #print(dev_indexes)
    reg_list = dict()
    for uniq in unique_devs:
        #print(uniq)
        reg_list[uniq] : List[RegInfoItem] = [RegInfoItem(**item) for a in reg_data for item in a['registers'] if a["device"] == uniq]
        

    for x in range(len(device_list)):
        device_list[x].reg_info = reg_list[device_list[x].dev_type] 
        
    return device_list, unique_ips , dev_indexes

def mod_read(func,reg, count, address, client ):
    if not func in func_dict:
        return
    fn = func_dict[func]
    try:
        x = fn(reg=reg, cnt=count, d_address= address, remote= client)
        return x    
    except (mb_ex.NoSuchSlaveException, mb_ex.ConnectionException, 
           mb_ex.ModbusIOException, mb_ex.NoSuchSlaveException, 
           mb_ex.TimeOutException) as e:
           log.error(e)
    return []        

def dicter(data, keys, indexes, scales):
    #print(len(data),len(keys), len(indexes))
    try:
        if len(data) >= indexes[-1] + 1: #chechking that modbus fetched data lenght longer than last index point!
            indexed_data =[data[i] for i in indexes]
            scaled = [indexed_data[i]*scales[i] for i in range(len(scales))]
            last_dict = {keys[i]: round(scaled[i],3) for i in range(len(indexes))}
            return last_dict
        else:
            print("provided data lenght is longer than last index number or vice versa")
    except Exception as e:
        print(e)        

def post_device_data(address, data, header):
    resp = json_post(address=address,data=data, header=header)
    return resp

def looper(devs, ips, index_list):
    y = list()
    temp_data = dict()
    data = dict()
    for ip, indexes in zip(ips,index_list):
        client = ModbusTcpClient(ip, 502)
        
        if client.connect():
            
            time.sleep(2)
            for indx in indexes:
                for register in devs[indx].reg_info:
                    #print(f"{ip} adresinde {devs[indx].mod_adrs} id'li cihaz okunuyor")
                    mod_resp = mod_read(register.typo, register.start_reg, register.count, devs[indx].mod_adrs,client=client)
                    #because the reading register addresses grouped to read (related and unrelated)
                    # we have that group's index numbers to get rid of unrelated register datas
                    if len(mod_resp) != 0:
                        temp_data = dicter(mod_resp,register.keys, register.index, register.scales)
                        data.update(temp_data)
                #print(data)
                try:
                    #print(url1 + devs[indx].dev_token + url2)
                    http_resp = post_device_data(url1 + devs[indx].dev_token + url2, data, headers) 
                    #print(http_resp)
                except Exception:
                    print(f"{t.now()} sunucuya erisim hatasi")
            client.close()
        else:
            print(f"{ip} is not responding. {t.now()}")    

def get_minute():
    return t.now().minute