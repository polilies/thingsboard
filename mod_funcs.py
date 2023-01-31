from pymodbus.client.sync import ModbusTcpClient
import struct
import ctypes

def tcp_modbus(ip, port):
    return ModbusTcpClient(ip, port)

def read_holding_S16(reg, cnt, d_address, remote):
    result = remote.read_holding_registers(reg, cnt, unit=d_address)
    if result.registers[0] > 32768:
       return ctypes.c_int((result.registers[0] ^ 0XFFFF)*-1).value
    else:
       return result.registers[0]

def read_input_S16(reg, cnt, d_address, remote):
    result = remote.read_input_registers(reg, cnt, unit=d_address)
    if result.registers[0] > 32768:
       return ctypes.c_int((result.registers[0] ^ 0XFFFF)*-1).value
    else:
       return result.registers[0]

def read_holding_S32(reg, cnt, d_address, remote):
        result = remote.read_holding_registers(reg, cnt*2, unit=d_address)
        regs = []
        for i in range(0,len(result.registers),2):
              regs.append(ctypes.c_long(((result.registers[i] << 16) | result.registers[i+1]) & 0XFFFFFFFF).value)
        return regs

def read_input_RS32(reg, cnt, d_address, remote):
        result = remote.read_input_registers(reg, cnt*2, unit=d_address)
        regs = []
        for i in range(0,len(result.registers),2):
              regs.append(ctypes.c_long(((result.registers[i+1] << 16) | result.registers[i]) & 0XFFFFFFFF).value)
        return regs

def read_holding_float(reg, cnt, d_address, remote):
        result = remote.read_holding_registers(reg, cnt*2, unit=d_address)
        regs = []
        for i in range(0,len(result.registers),2):
              raw = struct.pack('>HH',result.registers[i],result.registers[i+1])
              regs.append(struct.unpack('>f',raw)[0])
        return regs
        #raw = struct.pack('>HH', result.registers[0], result.registers[1])
        #return struct.unpack('>f',raw)[0]

def read_input_floatRwords(reg, cnt, d_address, remote):
        result = remote.read_input_registers(reg, cnt*2, unit=d_address)
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