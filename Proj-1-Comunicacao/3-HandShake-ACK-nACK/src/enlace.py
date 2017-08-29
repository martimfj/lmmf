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
        self.connect   = False
        self.loop = True
    
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

    ################################
    # Application  interface       #
    ################################
    def sendData(self, data):
        """ Send data over the enlace interface
        """
        #Construção do pack
        self.StructEop()
        self.StructHead()
        
#########################################################3
        #Envio do arquivo
        if (self.connect):
            pack = self.buildAckPacket(data)
            self.tx.sendBuffer(pack)


       # while (self.loop):
        if(self.getCommandType() == b"12"):
            pack = self.buildAckPacket()
            self.tx.sendBuffer(pack)

            pack = self.buildDataPacket(data)
            self.CalcularOverhead(pack,data)
            self.tx.sendBuffer(pack)
            self.loop = False;  
        else:
            pack = self.buildSynPacket()
            print("enviadooo")
            self.tx.sendBuffer(pack)
            time.sleep(0.1)

############################################################3                
        
    def getData(self):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        data, size = self.rx.unbuildDataPacket()
        return(data, len(data), size)
 

    #Define a estrutura do head
    def StructHead(self):
        self.headStart = 0xFF
        self.headStruct = Struct("start" / Int8ub, #Como é 16, o Head começará com \x00\xff + size 
                                 "size"/ Int16ub,
                                 "typeCommand"/ Int8ub)
        
    #Implementa o head
    def buildHead(self,dataLen,command):
        head = self.headStruct.build(dict(
                                start = self.headStart,
                                size = dataLen,
                                typeCommand = command)) 
        return head

    #Define a estrutura do eop
    def StructEop(self):
        self.endStart = 0xFF
        self.endStruct = Struct("c1" / Int8ub,
                                "c2"/ Int8ub,
                                "c3" / Int8ub,
                                "c4" /Int8ub)
    #Implementa o eop
    def buildEop(self):
        end = self.endStruct.build(dict(
                                c1 = 0x01,
                                c2 = 0x02,
                                c3 = 0x03,
                                c4 = 0x04))
        return end

    #PACOTE DADOS
    def buildDataPacket(self,data):
        DADO = 0
        pack = self.buildHead(len(data),DADO)
        pack += data
        pack += self.buildEop()
        print(len(data))
        return pack

    #PACOTE COMANDO SYN
    def buildSynPacket(self):
        SYN = 0x10
        pack = self.buildHead(0,SYN)
        pack += self.buildEop()
        return pack

    #PACOTE COMANDO ACK
    def buildAckPacket(self):
        ACK = 0x11
        pack = self.buildHead(0,ACK)
        pack += self.buildEop()
        return pack

    #PACOTE COMANDO NACK
    def buildNackPacket(self):
        NACK = 0x12
        pack = self.buildHead(0,NACK)
        pack += self.buildEop()
        return pack

    #CALCULAR OVERHEAD
    def CalcularOverhead(self,pack,data):
        overhead = len(pack)/len(data) 
        print("Overhead:" , overhead)
        return overhead   

    #OBTEM O TIPO DE COMANDO DO PACOTE
    def getCommandType(self):
        head = self.rx.buffer[:8]
        type = head
        print("TIPOOOOOOOOOOOOOOOooooooooOOO:" , head)
        return type 
    