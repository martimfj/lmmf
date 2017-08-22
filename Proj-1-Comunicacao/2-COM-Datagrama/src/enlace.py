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

    ################################
    # Application  interface       #
    ################################
    def sendData(self, data):
        """ Send data over the enlace interface
        """#######python med
        
        #Construção do pack
        self.StructEop()
        self.StructHead()
        
        #Envio do arquivo
        pack = self.buildDataPacket(data)
        self.tx.sendBuffer(pack)

    def getData(self, size):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        data = self.rx.getPacket()
        return(data, len(data))


    #Define a estrutura do head
    def StructHead(self):
        self.headStart = 0xFF
        self.headStruct = Struct("start" / Int16ub, #Como é 16, o Head começará com \x00\xff + size 
                                 "size"/ Int16ub)
        
    #Implementa o head
    def buildHead(self,dataLen):
        head = self.headStruct.build(dict(
                                start = self.headStart,
                                size = dataLen))    
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

    def buildDataPacket(self,data):
        pack = self.buildHead(len(data))
        pack += data
        pack += self.buildEop()
        return pack