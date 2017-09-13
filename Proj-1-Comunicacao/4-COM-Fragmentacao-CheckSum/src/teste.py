from construct import *
import binascii
import parser
import crcmod

imageR = "./imgs/imageC.png"
xBuffer = open(imageR, 'rb').read()
#print(xBuffer)


command = 0x10
data = b'\x54\xfd\xf4'
data1 = b''
dataLen = len(data1)
print(type(command))



headStart = 0xFF
headStruct = Struct("start" / Int16ub, #Como é 16, o Head começará com \x00\xff + size 
                    "size"/ Int16ub,
                    "typecommand"/ Int8ub)

crc8_func = crcmod.predefined.mkCrcFun('crc-8')
teste = int(hex(crc8_func(b'123456789')),16)
        
head = headStruct.build(dict(
                            start = headStart,
                            size = dataLen,
                            typecommand = command))

crc8_func = crcmod.predefined.mkCrcFun('crc-8')
crc = int(hex(crc8_func(head)),16)
print(crc)
print (int('0x10', 16))

# headcrcStruct = Struct("crc" / Int8ub) 
# headcrc = headcrcStruct.build(dict(crc = crc))

endStruct = Struct("c1" / Int8ub,
	                "c2"/ Int8ub,
	                "c3" / Int8ub,
	                "c4" / Int8ub)

end = endStruct.build(dict(
                        c1 = 0x01,
                        c2 = 0x02,
                        c3 = 0x03,
                        c4 = 0x04))


pack = head + data + end

# if head.startswith(b'\x00\xff'):
#     print(True)

# if end.startswith(b'\x01\x02'):
#     print(True)

print(head) #b'\x00\xff\x08\x00\x10'
print(end) #b'\x01\x02\x03\x04'
print(pack) #\x00\xff\x08\x00\x10\x01\x02\x03\x04'

eop = pack.find(b'\x01\x02\x03\x04') #Procura sequência pela byteArray
print(eop)
if eop != -1: #Se o EOP existe na byteArray
    head = pack[pack.find(b'\x00\xff'):5]
    size = int(binascii.hexlify(head[2:4]), 16)
    print(size)
    data = pack[5:eop]

# print(head[2:])
# print(binascii.hexlify(head[2:]))
# oi = binascii.hexlify(head[2:])
# print(int(oi, 16))


# https://www.dotnetperls.com/bytes-python
# https://construct.readthedocs.io/en/latest/basics.html
# https://stackoverflow.com/questions/509211/explain-slice-notation


crc8_func = crcmod.predefined.mkCrcFun('crc-8')
teste = hex(crc8_func(b'123456789'))
print(int(teste, 16).to_bytes(1, byteorder='big'))

# print(vai)
# # end += hex(vai)
# print(end)


# end =+ hex(teste)

#http://crccalc.com/
#http://crcmod.sourceforge.net/crcmod.html
#pip install crcmod