#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Prof. Rafael Corsi
#  Abril/2017
#  Aplicação
####################################################

from enlace import *
import time

# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)

def main():

    # Inicializa enlace
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    # Log
    print("-------------------------")
    print("Aguardando HandShake")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    com.bind()

    # Endereco da imagem a ser salva
    imageW = "./imgs/recebida.png"

    # Faz a recepção dos dados
    print ("Recebendo dados .... ")
    tempBuffer = com.getData()
    
    # log
    #print ("Lido              {} bytes ".format(nRx))

    # Salva imagem recebida em arquivo
    print("-------------------------")
    print ("Salvando dados no arquivo :")
    print (" - {}".format(imageW))
    f = open(imageW, 'wb')
    f.write(tempBuffer)

    # print("-------------------------")
    # print ("Log de recebimento:")
    # print ("Tamanho do arquivo: {} ".format(size))
    # print ("Tamanho do arquivo recebido: {} ".format(nRx))
    # print ("Perdas: {} ".format(size-nRx))

    
    # Finaliza o tempo e calcula o tempo de transmissão
    #print("O tempo total para a transmissão dos dados foi de: {}".format(fim - inicio))

    # Fecha arquivo de imagem
    f.close()

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

if __name__ == "__main__":
    main()