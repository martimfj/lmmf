from construct import *
import binascii
import parser
import crcmod


imageR = "./imgs/imageC.png"
data = open(imageR, 'rb').read()

headStart = 0xFF
dataLen = len(data)
command = 0x11
totalsize = 0xDD
crc_head_value = 0x00
crc_payload_value = 0x00

#-------------------------------------------------------------------------------------
headStruct = Struct("start" / Int16ub, #Como é 16, o Head começará com \x00\xff + size 
                    "size" / Int16ub,
                    "totaldatasize" / Int16ub,
                    "crc_head" / Int8ub,
                    "crc_payload" / Int8ub,
                    "typecommand" / Int8ub)
        
def buildHead(headStart, dataLen, totalsize,  crc_head_value, crc_payload_value, command):
	head = headStruct.build(dict(
	                    start = headStart,
	                    size = dataLen,
	                    totaldatasize = totalsize,
	                    crc_head = crc_head_value,
	                    crc_payload = crc_payload_value, #[7]
	                    typecommand = command))
	return head

#-------------------------------------------------------------------------------------
def crcCalcula(data):
	crc8_func = crcmod.predefined.mkCrcFun('crc-8')
	crc = crc8_func(data)
	return(crc)
#-------------------------------------------------------------------------------------
headinho = buildHead(headStart,dataLen,totalsize,0,0,0)
crcheadinho = crcCalcula(headinho)
crcdata = crcCalcula(data)

headzao = buildHead(headStart,dataLen,totalsize,crcheadinho,crcdata,0)

size = int(binascii.hexlify(headzao[2:4]), 16)
print(headzao)
CRC_head_value = headzao[7]
CRC_payload_value = headzao[6]
print(hex(headzao[7]))
print(hex(headzao[6]))

# dataByte = bytearray(data, encoding = "ascii")
# dataHex = binascii.hexlify(dataByte)

tsss = CRC_payload_value.to_bytes(2, byteorder='big')
print("yyyy", tsss)

# s=s.replace(b'PatientName',bytes(name))
headfff = headzao.replace(tsss, b'\x00')
print(headfff)

#-------------------------------------------------------------------------------------
eopStruct = Struct("c1" / Int8ub,
	               "c2"/ Int8ub,
	               "c3" / Int8ub,
	               "c4" / Int8ub)

eop = eopStruct.build(dict(
                        	c1 = 0x01,
                       		c2 = 0x02,
                        	c3 = 0x03,
                        	c4 = 0x04))
#-------------------------------------------------------------------------------------
# pack = head + bob + data + payloadCRC_value + eop