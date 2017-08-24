from construct import *
import binascii

headStart = 0xFF
headStruct = Struct("start" / Int16ub,
                    "size"/ Int16ub)
        

dataLen = 6969
head = headStruct.build(dict(start = headStart, size = dataLen))  

endStart = 0xFF
endStruct = Struct("c1" / Int8ub,
	                "c2"/ Int8ub,
	                "c3" / Int8ub,
	                "c4" /Int8ub)

end = endStruct.build(dict(
                                c1 = 0x01,
                                c2 = 0x02,
                                c3 = 0x03,
                                c4 = 0x04))


pack = head + end

if head.startswith(b'\x00\xff'):
    print(True)

if end.startswith(b'\x01\x02'):
    print(True)

print(head)
print(end)
print(head[2:])
print(binascii.hexlify(head[2:]))
oi = binascii.hexlify(head[2:])
print(int(oi, 16))


# https://www.dotnetperls.com/bytes-python
# https://construct.readthedocs.io/en/latest/basics.html
# https://stackoverflow.com/questions/509211/explain-slice-notation