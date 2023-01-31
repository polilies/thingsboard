from distutils.log import error
from http import client
from msilib.schema import Error
from operator import index
from pydoc import cli
import logging
#import requests

from mod_funcs import *
from conf_funcs import *
import time

logging.basicConfig(level=logging.INFO, filename="log.txt", filemode="a", format="%(asctime)s,%(levelname)s,%(message)s")
url1 = 'http://172.24.0.5:9090/api/v1/'
url2 = '/telemetry'
headers = {'Content-Type':'application/json'}
minutes =[0,10,20,30,40,50]

#test_data = {"temperature": 189.4, "humid":23.2}

   
#reads modbus device data and returns a dictionary of the read values
def read_dev(ip, port, dev_add, cnt,reg):
    try:
        client = tcp_modbus(ip,port)
        try:
            i = read_holding_float(reg=reg,cnt=cnt,d_address= dev_add, remote= client)
        except error:
            Print("no responce")       
    except Error:
        print("No connection")
    
    client.close()
    return i


def main() -> None:
    devices, reg_data = read_conf_sep()
    #print(url1 + dev[0].dev_token + url2)
    let = True
    while True:
        if (get_minute() in minutes) and let:
            for dev in devices:
                for reg in reg_data:
                    raw_data = read_dev(dev.ip,dev.port,dev.mod_address, reg_data[reg]['count'],reg['start_reg'])
                    data = dicter(raw_data,keys=dev[0].keys, indexes=dev[0].reg_indexes, scales=dev[0].scales)   
                    resp = post_device_data(url1 + dev[0].dev_token + url2, data, headers)  
                    #print(resp)
            let = False
        elif get_minute not in minutes:
            let = True
        
        time.sleep(30)
        
    
if __name__ == '__main__':
    main()