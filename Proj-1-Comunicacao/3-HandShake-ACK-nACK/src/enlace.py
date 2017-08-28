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

    def sendData(self, data):
        """ Send data over the enlace interface
        """

        #Construção do pack
        self.StructEop()
        self.StructHead()
        
        #Envio do arquivo
        pack = self.buildDataPacket(data)
        self.CalcularOverhead(pack,data)
        self.tx.sendBuffer(pack)

    def getData(self):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        _, data, _ = self.rx.getPacket()
        return(data)

#---------------------------------------------#
    #Define a estrutura do HEAD.
    def StructHead(self):
        self.headStart = 0xFF
        self.headStruct = Struct("start" / Int16ub, #Como é 16, o Head começará com \x00\xff + size 
                                 "size"/ Int16ub,
                                 "typecommand"/int8ub)
        
    #Implementa o head
    def buildHead(self,dataLen, command):
        head = self.headStruct.build(dict(
                                start = self.headStart,
                                size = dataLen,
                                typecommand = command)) 
        return head

#---------------------------------------------#
    #Define a estrutura do EOP.
    def StructEop(self):
        self.endStart = 0xFF
        self.endStruct = Struct("c1" / Int8ub,
                                "c2"/ Int8ub,
                                "c3" / Int8ub,
                                "c4" /Int8ub)

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
        pack = self.buildHead(len(data),0)
        pack += data
        pack += self.buildEop()
        print(len(data))
        return pack

#---------------------------------------------#
    #Cria o Pacote Comando Syn
    def buildSynPacket(self)
        SYN = b"10"
        pack = self.buildHead(0,SYN)
        pack += self.buildEop()
        return pack

    #Cria o Pacote Comando Ack
    def buildAckPacket(self)
        ACK = b"11"  
        pack = self.buildHead(0,ACK)
        pack += self.buildEop()
        return pack

    #Cria o Pacote Comando nAck
    def buildNackPacket(self)
        NACK = b"12"
        pack = self.buildHead(0,NACK)
        pack += self.buildEop()
        return pack

#---------------------------------------------#
    #Classifica o pacote em Commandos ou Dado
    def getPacketType(self):
        head, _, _ = self.rx.getPacket()
        if head.endswith(b'0')
            return ("Dado")
        elif head.endswith(b'10') or head.endswith(b'11') or head.endswith(b'12')
            return ("Comando")
        else:
            return ("Erro")

    #Classifica o comando em Syn, Ack ou nAck
    def getCommandType(self):
        head, _, _ = self.rx.getPacket()
        if head.endswith(b'10') 
            return("SYN")
        elif head.endswith(b'11')
            return ("ACK")
        elif head.endswith(b'12')
            return ("nACK")

    #Pega o size expresso no Head
    def getSize(self):
        head, _, _ = self.rx.getPacket()
        size = int(binascii.hexlify(head[2:4]), 16)
        return (size)

#---------------------------------------------#
    #CALCULAR OVERHEAD
    def CalcularOverhead(self,pack,data):
        overhead = len(pack)/len(data) 
        print("Overhead:" , overhead)
        return overhead





