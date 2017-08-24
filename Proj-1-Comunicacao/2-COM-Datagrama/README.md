---
title: Camada Física -  Datagrama : 
date: 2017
---

# Projeto 
Essa etapa do projeto consiste na criação de um protocolo de comunicação entre o client e o server, deixando de ser um streaming de dados brutos, sem nenhuma manipulação e passa a conter um encapsulamento dos dados em um pacote ou (datagrama), o que fornece envios de imagens de forma mais segura.

## Streaming Bruto
Os principais problemas da comunicação através de um Straming bruto surgem quando se tem a transferência de mais de um arquivo ou arquivos pesados. 

Imagine a situação em que há perda de bytes em uma transmissão, como não é possível identificar quando uma imagem termina e outra começa, a imagem 1 será construída com partes da imagem 2. Através dessa simulação pode-se afirmar que esse método de transferência possui dois problemas, ou seja, os dados se misturam em casos de perdas, e não é possível detectar a perdas de dados.
  
## Encapsulamento
Encapsulamento é o tipo de transferência utilizado como solução para os problemas do streaming bruto, visto que em um pacote, possui um cabeçalho (head) e um fim do pacote (eop), que permitem delimitar o começo de um fluxo de dados. Um arquivo grande pode ser dividido em vários pacotes pequenos, o que diminui a perda de dados em um fluxo.

## HEAD e EOP utilizados
#imagem

O head possui 4 bytes reservados, os dois primeiros bytes contem a marcação de inicialização, e os dois últimos bytes contém o tamanho do arquivo a ser empacotado

O eop possui 4 bytes reservados, que fornecem uma sequência para indicar o final do arquivo, sequencias razoavelmente grandes no eop evitam que o payload contenha a mesma sequência, favorecendo a transferência do pacote completo 

## OverHead
Definido a quantidade de bytes reservados para a parte de controle do pacote, pose-se calcular o protocolo overhead, que é a razão do tamanho total do pacote pelo tamanho de sua carga útil, quanto maior o overhead maior e a eficiência do protocolo.

Para um arquivo de 3093 bytes foi obtido:
OverHead = 

## BaudRate
O baudRate é a taxa em bits por segundo que uma rede consegue transmitir bits

## Troughput
troughput e a velocidade de envio de um dado pela rede

