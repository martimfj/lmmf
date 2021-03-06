from construct import *
import binascii
import parser


command = 0x10
data = b'\x54\xfd\xf4'
data1 = b''
dataLen = len(data1)

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

eop = pack.find(b'\x01\x02\x03\x04') #Procura sequência pela byteArray
print(eop)
if eop != -1: #Se o EOP existe na byteArray
    head = pack[pack.find(b'\x00\xff'):5]
    size = int(binascii.hexlify(head[2:4]), 16)
    print(size)
    data = pack[5:eop]


print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMNhhhhhmMMMMMMdhhhhhhhMMMMMMMMMMMMMhhhhhhhdMMMMMMMMMMMMdyyyyyydMMMMMMMMMMMMMMMMMMMNdyssoossydNMMMMMMMMdhhhhhhhhhhhhhhdMMMMMdhhhhhhhMMMMMMMMMMMMMhhhhhhhdMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMm     +MMMMMM:       sMMMMMMMMMMMs       -MMMMMMMMMMMm`      `mMMMMMMMMMMMMMMNy/`            `oMMMMMM:              :MMMMM-       sMMMMMMMMMMMo       -MMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMm     +MMMMMM:       `mMMMMMMMMMm        -MMMMMMMMMMM-        -MMMMMMMMMMMMN+`       `...    .NMMMMMM:              :MMMMM-       `mMMMMMMMMMm        -MMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMm     +MMMMMM:    .   :MMMMMMMMM-   .    -MMMMMMMMMMo    ++    oMMMMMMMMMMd.     .odMMMMMMNdsmMMMMMMM:     MMMMMMMMMMMMMMM-    .   :MMMMMMMMM-   .    -MMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMm     +MMMMMM:    y    yMMMMMMMs   `s    -MMMMMMMMMd    `NN.    dMMMMMMMMN`     sMMMMMMMMMMMMMMMMMMMM:     MMMMMMMMMMMMMMM-    y    yMMMMMMMs   `y    -MMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMm     +MMMMMM:    m/   `NMMMMMm    hs    -MMMMMMMMN.    yMMh    .NMMMMMMM+     oMMMMMMMMMMMMMMMMMMMMM:     mNNNNNNNNMMMMMM-    m/   .NMMMMMm    hs    -MMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMm     +MMMMMM:    dN`   +MMMMM-   /Ms    -MMMMMMMM/    -MMMM/    /MMMMMMM.     NMMMMyooooooooooMMMMMM:              MMMMMM-    dm`   +MMMMM-   /Mo    -MMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMm     +MMMMMM:    hMs    dMMMs   `NMo    -MMMMMMMy     mMMMMN`    yMMMMMM`    `MMMMM/          MMMMMM:              MMMMMM-    hMs    dMMMs   `NMo    -MMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMm     +MMMMMM:    hMM-   -MMm`   yMMo    -MMMMMMm`    .++++++.    `mMMMMM-     NMMMMo----`     MMMMMM:     dddddddddMMMMMM-    hMM-   -MMm`   hMMo    -MMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMm     +MMMMMM:    hMMd    sM-   /MMMo    -MMMMMM:                  -MMMMMo     oMMMMMMMMM+     MMMMMM:     MMMMMMMMMMMMMMM-    hMMd    sM-   /MMMo    -MMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMm     +MMMMMM:    hMMM+   `+   `NMMMo    -MMMMMs     ----------     oMMMMN.     oNMMMMMMM+     MMMMMM:     MMMMMMMMMMMMMMM-    hMMM+   `+   `NMMMo    -MMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMm     +MMMMMM:    hMMMN.       yMMMMo    -MMMMd     :MMMMMMMMMM/     dMMMMm-     `/shdhhy:     MMMMMM:     ssssssssshMMMMM-    hMMMN`       yMMMMo    -MMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMm     +MMMMMM:    hMMMMy      /MMMMMo    -MMMN.    `mMMMMMMMMMMm`    .NMMMMMs.                 MMMMMM:              :MMMMM-    hMMMMy      /MMMMMo    -MMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMm`````oMMMMMM:````hMMMMM/````.NMMMMMo````:MMMo`````sMMMMMMMMMMMMs`````oMMMMMMMdo:.`      `.-:+sMMMMMM/``````````````/MMMMM:````hMMMMM/````.NMMMMMo````:MMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNNNNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMNNNNNNNNNNNMMMMMMMMMMMMMMNNNNNNNNNNNNNNNNMMMMMMMMMMMMNmdhhhdmNMMMMMMMMNNNNNNNNNNNNNNNMMMMMMNNNNNNNNNNNMMMMMMMMMMMMMMNNNNNNMMMMMMNNNNNNNNNNNMMMMMMMMMMMMMMMMMMMMMMMmmmmmmmMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMs           `-/sNMMMMMMMM-              +MMMMMMMMNy/.         `:oNMMMN               yMMMMN            `.:+hMMMMMMMN     /MMMMMM/           `./odMMMMMMMMMMMMMMMMy       sMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMs                +MMMMMMM-              +MMMMMMN+`              +MMMMN               yMMMMN                 .mMMMMMN     /MMMMMM/                `+NMMMMMMMMMMMMm`        dMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMs     ydddho-     +MMMMMM-    `dddddddddmMMMMMd.     :ydNNNmho::MMMMMN     /dddddddddNMMMMN     /ddddhs:     -MMMMMN     /MMMMMM/     dddddyo:     `sMMMMMMMMMMM-    y    .NMMMMMMMMMMMMMMMMMM
MMMMMMMMMMs     dMMMMMM.    `MMMMMM-    .MMMMMMMMMMMMMMN`    `hMMMMMMMMMMMMMMMMN     +MMMMMMMMMMMMMMN     oMMMMMMM.    `MMMMMN     /MMMMMM/     MMMMMMMMm-     sMMMMMMMMMo    /Mo    +MMMMMMMMMMMMMMMMMM
MMMMMMMMMMs     dMMMMMN.    .MMMMMM-    .MMMMMMMMMMMMMM+     yMMMMMMMMMMMMMMMMMN     +MMMMMMMMMMMMMMN     oMMMMMNs     +MMMMMN     /MMMMMM/     MMMMMMMMMN.     NMMMMMMMd    `NMM.    hMMMMMMMMMMMMMMMMM
MMMMMMMMMMs     sdhhy+`    `dMMMMMM-     ````````.MMMMM`    `MMMMMMMMMMMMMMMMMMN      ````````+MMMMMN     `....`     -yMMMMMMN     /MMMMMM/     MMMMMMMMMMo     yMMMMMMN.    sMMMh    `NMMMMMMMMMMMMMMMM
MMMMMMMMMMs              `+NMMMMMMM-             `MMMMM     -MMMMMMMMMMMMMMMMMMN              /MMMMMN               -+hMMMMMMN     /MMMMMM/     MMMMMMMMMMy     oMMMMMM/    -MMMMM/    :MMMMMMMMMMMMMMMM
MMMMMMMMMMs             oMMMMMMMMMM-    `yyyyyyyyyMMMMM`    `MMMMMMMMMMMMMMMMMMN     -yyyyyyyyhMMMMMN     :yyyyso:     -NMMMMN     /MMMMMM/     MMMMMMMMMM+     yMMMMMy     +ssssso     sMMMMMMMMMMMMMMM
MMMMMMMMMMs     dNNh`    +MMMMMMMMM-    .MMMMMMMMMMMMMM:     dMMMMMMMMMMMMMMMMMN     +MMMMMMMMMMMMMMN     oMMMMMMMs     oMMMMN     /MMMMMM/     MMMMMMMMMN`    `NMMMMm`                  dMMMMMMMMMMMMMM
MMMMMMMMMMs     dMMMm-    -mMMMMMMM-    .MMMMMMMMMMMMMMd     .mMMMMMMMMMMMMMMMMN     +MMMMMMMMMMMMMMN     oMMMMMMMy     /MMMMN     /MMMMMM/     MMMMMMMMh.     yMMMMM-     `````````     .NMMMMMMMMMMMMM
MMMMMMMMMMs     dMMMMN/    `yMMMMMM-    `dddddddddmMMMMMy      /ymNNNmdys/dMMMMN     :dddddddddNMMMMN     /ddddhy/      hMMMMN     /MMMMMM/     ddddhs+.     `hMMMMMo     yMMMMMMMMMh     +MMMMMMMMMMMMM
MMMMMMMMMMs     dMMMMMMs     /NMMMM-              +MMMMMMd-               hMMMMN               yMMMMN                 .hMMMMMN     /MMMMMM/                .oNMMMMMd     :MMMMMMMMMMM/     hMMMMMMMMMMMM
MMMMMMMMMMs     dMMMMMMMh`    .dMMM-              +MMMMMMMMdo-`         `:dMMMMN               yMMMMN             `-+hMMMMMMMN     /MMMMMM/           .-/smMMMMMMMN.     mMMMMMMMMMMMN`    `NMMMMMMMMMMM
MMMMMMMMMMNNNNNNMMMMMMMMMNNNNNNNMMMNNNNNNNNNNNNNNNNMMMMMMMMMMMMNddhhddmNMMMMMMMMNNNNNNNNNNNNNNNMMMMMMNNNNNNNNNNNNMMMMMMMMMMMMMNNNNNNMMMMMMNNNNNNNNNNNMMMMMMMMMMMMMMNNNNNNMMMMMMMMMMMMMNNNNNNNMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")

# print(head[2:])
# print(binascii.hexlify(head[2:]))
# oi = binascii.hexlify(head[2:])
# print(int(oi, 16))


# https://www.dotnetperls.com/bytes-python
# https://construct.readthedocs.io/en/latest/basics.html
# https://stackoverflow.com/questions/509211/explain-slice-notation