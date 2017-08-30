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
import sys
import os

# Threads
import threading

import binascii

# Class
class RX(object):
    """ This class implements methods to handle the reception
        data over the p2p fox protocol
    """
    
    def __init__(self, fisica):
        """ Initializes the RX class
        """
        self.fisica      = fisica
        self.buffer      = bytes(bytearray()) #buffer de bytes
        self.threadStop  = False
        self.threadMutex = True
        self.READLEN     = 1024
        self.packetFound = False

    def thread(self):
        """ RX thread, to send data in parallel with the code
        """
        while not self.threadStop:
            if(self.threadMutex == True): #Mutex é um semafóro que determina quem ta manipulando o buffer.
                rxTemp, nRx = self.fisica.read(self.READLEN)
                if (nRx > 0):
                    self.buffer += rxTemp
                time.sleep(0.001)

            #Recebe todos os pacotes, salva no buffer e fica varrendo o buffer em procura do EOP,
            # manda os dados de head, eop e payload para o enlace tratar e montar tudo.

    def threadStart(self):
        """ Starts RX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill RX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the RX thread to run

        This must be used when manipulating the Rx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the RX thread (after suspended)
        """
        self.threadMutex = True

    def getIsEmpty(self):
        """ Return if the reception buffer is empty
        """
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self):
        """ Return the total number of bytes in the reception buffer
        """
        return(len(self.buffer))

    def getAllBuffer(self, len):
        """ Read ALL reception buffer and clears it
        """
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self, nData):
        """ Remove n data from buffer
        """
        self.threadPause()
        b           = self.buffer[0:nData]
        self.buffer = self.buffer[nData:]
        self.threadResume()
        return(b)

    def getNData(self, size):
        """ Read N bytes of data from the reception buffer

        This function blocks until the number of bytes is received
        """

        while(self.getBufferLen() < size):
            # sys.stdout.write(str(self.getBufferLen()) + "/" + str(size))
            # sys.stdout.write("\r")
            # sys.stdout.flush()
            time.sleep(0.05)

        # sys.stdout.write(str(self.getBufferLen()) + "/" + str(size))
        # sys.stdout.write("\r")

        return(self.getBuffer(size))

    def clearBuffer(self):
        """ Clear the reception buffer
        """
        self.buffer = b""

    def getPacket(self):
        while(self.packetFound == False):
            eop = self.buffer.find(b'\x01\x02\x03\x04') #Procura sequência pela byteArray
            if eop != -1: #Se o EOP existe na byteArray
                self.packetFound = True
                head = self.buffer[self.buffer.find(b'\x00\xff'):5]
                payload = [head:eop]
                return head, payload, eop

