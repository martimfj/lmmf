from construct import *
import binascii
import parser

dataLen = 2*1024
command = 0x10
data = b'\x54\xfd'

headStart = 0xFF
headStruct = Struct("start" / Int16ub, #Como é 16, o Head começará com \x00\xff + size 
                    "size"/ Int16ub,
                    "typecommand"/ Int8ub)
        
head = headStruct.build(dict(
                            start = headStart,
                            size = dataLen,
                            typecommand = command))

endStruct = Struct("c1" / Int8ub,
	                "c2"/ Int8ub,
	                "c3" / Int8ub,
	                "c4" /Int8ub)

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

print(pack[pack.find(b'\x00\xff'):5])
print(head[-1])
print(head)
print(head[4:5])
SYN = b"10"
print(SYN)
# print(head[2:])
# print(binascii.hexlify(head[2:]))
# oi = binascii.hexlify(head[2:])
# print(int(oi, 16))


# https://www.dotnetperls.com/bytes-python
# https://construct.readthedocs.io/en/latest/basics.html
# https://stackoverflow.com/questions/509211/explain-slice-notation