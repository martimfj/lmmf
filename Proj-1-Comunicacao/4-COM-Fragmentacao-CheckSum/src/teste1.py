import crcmod
import binascii



imageR = "./imgs/imageB.png"
xBuffer = open(imageR, 'rb').read()
#print(xBuffer)

crc8_func = crcmod.predefined.mkCrcFun('crc-8')
print(hex(crc8_func(xBuffer)))
crc = int(hex(crc8_func(xBuffer)), 16).to_bytes(1, byteorder='big')
print(crc)


hex_str = "0xf4"
print(type(hex_str))
hex_int = int(hex_str, 16)
#print(bytes(hex_int))
print((hex_int).to_bytes(1, byteorder='big'))
new_int = hex_int
teste = hex(new_int)
print (hex(new_int)[1:])
print(teste)
print(type(teste))


# binary_string = binascii.unhexlify(hex_int)
# print(binary_string)
# print(type(binary_string))