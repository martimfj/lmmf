#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Prof. Rafael Corsi
#  Abril/2017
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time
import parser
import binascii
import crcmod

# Construct Struct
from construct import *

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX

class enlace(object):
    """ This class implements methods to the interface between Enlace and Application
    """

    def __init__(self, name):
        """ Initializes the enlace class
        """
        self.fisica      = fisica(name)
        self.rx          = RX(self.fisica)
        self.tx          = TX(self.fisica)
        self.connected   = False
        self.enviardata  = False
        self.corrupt     = False
        self.bufferdata  = bytes(bytearray())
        self.sizeselect  = 2048
        self.datasize    = 0
        self.sizepack    = 0
         
    def enable(self):
        """ Enable reception and transmission
        """
        self.fisica.open()
        self.rx.threadStart()
        self.tx.threadStart()

    def disable(self):
        """ Disable reception and transmission
        """
        self.rx.threadKill()
        self.tx.threadKill()
        time.sleep(1)
        self.fisica.close()
        
    def fragment(self,data):
        #print("tamanhor bufferdataAAAA", len(self.bufferdata))
        if (len(self.bufferdata) >= self.sizeselect):
            b           = self.bufferdata[:self.sizeselect]
            self.bufferdata = self.bufferdata[self.sizeselect:]
        else:
            b           = self.bufferdata[:]
            self.bufferdata = b""
        #print("tamanhor b", len(b)) 
        return self.buildDataPacket(b)

    def connect(self,data):
        self.constructado()
        self.bufferdata = data[:]
        self.datasize = len(data)
        """ Estabelece um conexão confiável com o Servidor - Máquina de Estados Client """
        print("Client - Iniciando Handshake")

        while(self.connected == False):
            print("Enviando SYN...")
            self.sendData(self.buildSynPacket())
            print("SYN Enviado!")
            print("Esperando pelo ACK + SYN do Servidor...")
            time.sleep(0.15) 
            if(self.getCommandType() == "ACK"):
                print("Ack recebido")
                time.sleep(0.15)
                if (self.getCommandType() == "SYN"): 
                    print("SYN Recebido!")
                    print("Confirmando recebimento do SYN...")
                    self.sendData(self.buildAckPacket())    
                    print("Conexão estabelecida!")
                    self.connected = True
            elif(self.getCommandType() == "Erro"):
                print("Erro na transmissão de dados. Reconectando...")
            else:
                print("Time out")
                print("Reiniciando conexão")
                time.sleep(0.2)

        while(len(self.bufferdata)!= 0):
            pack = self.fragment(data)
            while(self.enviardata == False):
                self.sendData(pack)
                print("Enviado:",len(pack), "Bytes")
                time.sleep(0.3)
                if (self.getCommandType() == "ACK"):
                    self.enviardata = True
                elif(self.getCommandType() == "nACK"):
                    self.enviardata = False
            self.enviardata = False
            print("Proximo Pacote")
            time.sleep(0.2)        
            
    def bind(self):
        self.constructado()
        """ Estabelece um conexão confiável com o Client - Máquina de Estados Servidor """
        print("Servidor - Iniciando Handshake")
        while(self.connected == False):
            print("Aguardando um Comando do Client")
            if(self.getCommandType() == "SYN"):
                print("SYN Recebido!")

                self.sendData(self.buildAckPacket())
                print("ACK Enviado")
                time.sleep(0.1)

                self.sendData(self.buildSynPacket())
                print("SYN Enviado")

                if(self.getCommandType() == "ACK"):
                    print("ACK Recebido!")
                    self.connected = True
                    print("Conexão estabelecida!")

                time.sleep(0.2)

            elif(self.getCommandType() == "nACK"):
                print("Conexão não estabelecida, erro!")
                self.sendData(self.buildNackPacket())

            elif(self.getCommandType() == "Erro"):
                print("Erro na transmissão de dados.")
                self.sendData(self.buildNackPacket())

            else:
                print("Timeout! O Client não respondeu no tempo hábil. Reiniciando Conexão.")
                self.sendData(self.buildNackPacket())
            time.sleep(0.15)

    def constructado(self):
        self.StructEop()
        self.StructHead()

    def sendData(self, pack):
        self.tx.sendBuffer(pack)
            
    def getData(self):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        byterecebido = 0
        bytetotal = 1
        f = bytes(bytearray())

        while(byterecebido != bytetotal):
            head, data = self.rx.getPacket()
            size = int(binascii.hexlify(head[2:4]), 16)
            CRC_Head = self.getCRC(head[:7])
            CRC_Data = self.getCRC(data)
            print("Size: ",size,"/",len(data))
            print("CRC_HEAD: ",CRC_Head,"/",head[7])
            print("CRC_DATA: ",CRC_Data,"/",head[8])

    
            if(size != len(data) or (CRC_Head != head[7]) or (CRC_Data != head[8]) ):
                print("Arquivo corrompido")
                print("nAck Enviado")
                self.sendData(self.buildNackPacket())
                time.sleep(0.2)

            else:  
                byterecebido += len(data) ## verificar len no packote
                bytetotal = int(binascii.hexlify(head[4:6]), 16)
                print("Bytes recebidos: ",byterecebido,"/",bytetotal)
                print("ACK Enviado")
                self.sendData(self.buildAckPacket())
                f += data
                time.sleep(0.2) 
        return f

#---------------------------------------------#
    #Define a estrutura do HEAD.
    def StructHead(self):
        self.headStart = 0xFF
        self.headStruct = Struct("start" / Int16ub, #Como é 16, o Head começará com \x00\xff + size 
                                "size" / Int16ub,
                                "totaldatasize" / Int16ub,
                                "typecommand" / Int8ub,
                                "crc_head" / Int8ub,
                                "crc_payload" / Int8ub
                                )
        
    #Implementa o head
    def buildHead(self, dataLen, totalsize, command, crc_head_value, crc_payload_value):
        head = self.headStruct.build(dict(
                                start = self.headStart,
                                size = dataLen,
                                totaldatasize = totalsize,
                                typecommand = command,
                                crc_head = crc_head_value,
                                crc_payload = crc_payload_value))
        return head

#---------------------------------------------#
    #Define a estrutura do EOP.
    def StructEop(self):
        self.endStart = 0xFF
        self.endStruct = Struct("c1" / Int8ub,
                                "c2" / Int8ub,
                                "c3" / Int8ub,
                                "c4" / Int8ub)

    #Implementa o EOP.
    def buildEop(self):
        end = self.endStruct.build(dict(
                                c1 = 0x01,
                                c2 = 0x02,
                                c3 = 0x03,
                                c4 = 0x04))
        return end

#---------------------------------------------#
    #Cria o Pacote de Dados.
    def buildDataPacket(self,data):
        size = len(data)       
        head = self.buildHead(size,self.datasize,0,0,0)

        CRC_Head = self.getCRC(head[:7])
        CRC_Data = self.getCRC(data)

        head = self.buildHead(size,self.datasize,0,CRC_Head,CRC_Data)

        pack = head + data
        pack += self.buildEop()
        return pack
#---------------------------------------------#
    #Cria o Pacote Comando Syn
    def buildSynPacket(self):
        SYN = 0x10
        pack = self.buildHead(0,0,SYN,0,0)
        pack += self.buildEop()
        return pack

    #Cria o Pacote Comando Ack
    def buildAckPacket(self):
        ACK = 0x11  
        pack = self.buildHead(0,0,ACK,0,0)
        pack += self.buildEop()
        return pack

    #Cria o Pacote Comando nAck
    def buildNackPacket(self):
        NACK = 0x12
        pack = self.buildHead(0,0,NACK,0,0)
        pack += self.buildEop()
        return pack

#---------------------------------------------#
    #Classifica o pacote em Commandos ou Dado
    def getPacketType(self):
        head, _= self.rx.getPacket()
        if head.endswith(b'\x00'):
            return ("Dado")
        elif head.endswith(b'\x10') or head.endswith(b'\x11') or head.endswith(b'\x12'):
            return ("Comando")
        else:
            return ("Buffer vazio")

    #Classifica o comando em Syn, Ack ou nAck
    def getCommandType(self):
        if (self.rx.getIsEmpty() == False):
            head, _= self.rx.getPacket()
            print(head)
            print(head[6])
            if (head[6] == 16):
                return ("SYN")
            elif (head[6] == 17):
                return ("ACK")
            elif (head[6] == 18):
                return ("nACK")
            else:
                return ("Erro")
        else:
            time.sleep(0.5)
            return("Erro")

    #Pega o size expresso no Head
    def getSize(self,data):
        size = int(binascii.hexlify(data[2:4]), 16)
        return (size)         

#---------------------------------------------#
    #CALCULAR OVERHEAD
    def CalcularOverhead(self, pack, data):
        overhead = len(pack)/len(data) 
        print("Overhead:" , overhead)
        return (overhead)

#---------------------------------------------#
    #Calcula CRC
    def getCRC(self, data):
        crc8_func = crcmod.predefined.mkCrcFun('crc-8')
        crc = crc8_func(data)
        return(crc)