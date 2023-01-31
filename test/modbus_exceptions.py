from mod_funcs_exc_log import *
from pymodbus import exceptions as mb_ex 
import time

import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT,filename="modbus_errorlog.txt")
log = logging.getLogger()
log.setLevel(logging.DEBUG)

#reads modbus device data and returns a dictionary of the read values
def read_dev(ip: str, port: int, dev_add: int, cnt: int,reg: int) -> list:
    
    client = tcp_modbus(ip,port)
    try:
        
        i = read_holding_float(reg=reg,cnt=cnt,d_address= dev_add, remote= client)
        return i    
    except (mb_ex.NoSuchSlaveException, mb_ex.ConnectionException, 
            mb_ex.ModbusIOException, mb_ex.NoSuchSlaveException, 
            mb_ex.TimeOutException) as e:
            log.error(e)
            
            return []
    finally:
        client.close()



#for _ in range(3):        
#    print(read_dev('10.46.111.6',502, 2, 3, 19000))
#    time.sleep(5)