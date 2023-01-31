from pymodbus.client.sync import ModbusTcpClient
import struct
import ctypes
import logging
from datetime import datetime as ti
'''
logger_1 = logging.getLogger("pymodbus.client")
logger_1.setLevel(logging.ERROR)
handler_1 = logging.FileHandler("mod_log.txt")
formatter1 = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler_1.setFormatter(formatter1)
logger_1.addHandler(handler_1)
'''
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT,filename="modbus_errorlog.txt")
log = logging.getLogger()
log.setLevel(logging.ERROR)

illegals = {1:'Illegal Function', 2: 'Illegal Data Address', 3: 'Illegal Data Value', 
            4: 'Slave Device Failure', 5: 'Acknowledge', 6: 'Slave Device Busy', 
            7: 'Negative Acknowledge', 8: 'Memory Parity Error', 10: 'Gateway Path Unavailable',
            11: 'Gateway Target Device Failed to Respond'}

def tcp_modbus(ip, port):
    return ModbusTcpClient(ip, port)

#this function can read from ION7650 properly.
def read_holding_S16(reg, cnt, d_address, remote):
    result = remote.read_holding_registers(reg, cnt, unit=d_address)
    regs=[]
    if result.isError():                           
        print(f'Modbus Error: {result}, means there is no proper response, {ti.now()}')
        return regs
    else:
        for i in range(0,len(result.registers),1):
                if result.registers[i] > 32768:
                        regs.append(ctypes.c_int((result.registers[i] ^ 0XFFFF)*-1).value)
                else:
                        regs.append(result.registers[i])

        return regs

def read_input_S16(reg, cnt, d_address, remote):
    result = remote.read_input_registers(reg, cnt, unit=d_address)
    if result.registers[0] > 32768:
       return ctypes.c_int((result.registers[0] ^ 0XFFFF)*-1).value
    else:
       return result.registers[0]

def read_holding_S32(reg, cnt, d_address, remote):
        result = remote.read_holding_registers(reg, cnt*2, unit=d_address)
        regs = []
        if result.isError():
                print(f'Modbus Error: {result}, means there is no proper response, {ti.now()}')
                return regs
        else:
            for i in range(0,len(result.registers),2):
                regs.append(ctypes.c_long(((result.registers[i] << 16) | result.registers[i+1]) & 0XFFFFFFFF).value)
            return regs

def read_holding_RS32(reg, cnt, d_address, remote):
        result = remote.read_holding_registers(reg, cnt*2, unit=d_address)
        regs = []
        for i in range(0,len(result.registers),2):
              regs.append(ctypes.c_long(((result.registers[i+1] << 16) | result.registers[i]) & 0XFFFFFFFF).value)
        return regs

def read_input_RS32(reg, cnt, d_address, remote):
        result = remote.read_input_registers(reg, cnt*2, unit=d_address)
        regs = []
        for i in range(0,len(result.registers),2):
              regs.append(ctypes.c_long(((result.registers[i+1] << 16) | result.registers[i]) & 0XFFFFFFFF).value)
        return regs

def read_holding_float(reg, cnt, d_address, remote):
        #try:
        result = remote.read_holding_registers(reg, cnt*2, unit=d_address)
        regs = []
        if result.isError():
                print(f'Modbus Error: {result}, means there is no proper response. {ti.now()}')
                return regs
        else:
                for i in range(0,len(result.registers),2):
                        raw = struct.pack('>HH',result.registers[i],result.registers[i+1])
                        regs.append(struct.unpack('>f',raw)[0])
                return regs
        #raw = struct.pack('>HH', result.registers[0], result.registers[1])
        #return struct.unpack('>f',raw)[0]
'''        
        except (mb_ex.NoSuchSlaveException, mb_ex.ConnectionException, mb_ex.ModbusIOException, mb_ex.NoSuchSlaveException) as e:
                logger_1.debug("An exception has raised!")
        except mb_ex.ExceptionResponse as e:
                logger_1.debug(e)
        finally:
                remote.close()
'''        


def read_input_floatRwords(reg, cnt, d_address, remote):
        result = remote.read_input_registers(reg, cnt*2, unit=d_address)
        regs = []
        for i in range(0,len(result.registers),2):
              raw = struct.pack('>HH', result.registers[i+1], result.registers[i])
              regs.append(struct.unpack('>f',raw)[0])
        return regs

def read_holding_floatRwords(reg, cnt, d_address, remote):
        result = remote.read_holding_registers(reg, cnt*2, unit=d_address)
        regs = []
        for i in range(0,len(result.registers),2):
              raw = struct.pack('>HH', result.registers[i+1], result.registers[i])
              regs.append(struct.unpack('>f',raw)[0])
        return regs

def read_holding_float1(reg, cnt, d_address, remote):
    result = remote.read_holding_registers(reg, cnt * 2, unit=d_address)
    raw = struct.pack('>HH', result.registers[0], result.registers[1])
    return struct.unpack('>f', raw)[0]

def write_register(reg, data, d_address, remote):
        remote.write_register(reg, data, unit=d_address)
        

def convertion(deger, oran):
        return deger/oran