# Camada Física - Projeto 1 - COM-Fragmentação e CheckSum
Leonardo Medeiros e Martim Ferrera José

Nessa etapa do projeto, foi implementado a fragmentação dos dados na camada de enlace para possibilitar o reenvio mais eficiente dos dados, caso um alguma anomalia for detectada. Para a detecção de anomalias (erros) na transmissão, foi implementado um CRC (*Cyclic redundancy check*) para o *Head* e outro para o *payload*. O Servidor analisa os CRC's e envia um ACK/NACK em resposta se o pacote foi recebido corretamente ou não.

## Funcionamento da Fragmentação
A fragmentação dos dados é um métedo de minimização de erros, visto que a probabilidade de um dado ser corrompido nos pacotes maiores é grande. Além disso, quando se fragmenta um dado em pacotes de tamanho menor é possível tratar eventuais erros e pacotes corrompidos, reenviando somente aquele determinado pacote ao invés do dado todo.

Foi estabelecido um tamanho fixo para os pacotes, todos tem no máximo *2048 bytes*. Os dados são recortados no *buffer* do *client* e enviados separadamente de acordo com a resposta do *Server* (ACK ou NACK). Se o *Server* responde o recebimento do pacote com um ACK, o Client envia o próximo pacote. Caso receba um NACK, ele reenvia o pacote anterior.

## Funcionamento do CRC
O *cyclic redundancy check* (CRC) é um método de detecção de erros, que detecta a mudança acidental em cadeia de dados. Esse algoritmo baseia-se na divisão de polinômios, isto é, ele interpreta os dados como se fossem coeficientes de um polinômio e realiza uma divisão binária aplicando um XOR a cada termo. Ou seja, nesta divisão o dividendo é igual aos dados, o divisor é o polinômio "chave" e o resto da divisão é igual ao CRC. 

:exclamation: `Quanto mais complexo (maior o grau) do polinômio, melhor será o tratamento do erro. `

O polinômio escolhido para servir como "chave", foi *x^8+x^2+x^1+1*, que se traduz em binário para `0x107`, que é o **CRC-8**.

Este polinômio foi escolhido por ser muito simples e eficiente, resultando em um CRC de apenas 8 bits de tamanho, resultando em um menor Overhead, comparando com outros CRC's de maior grau.

Neste protocolo, o CRC é calculado em cada pacote, para o Head e para o Payload a fim de detectar erros nestes dois lugares.

Para implementar o CRC, foi utilizado o pacote [crcmod](http://crcmod.sourceforge.net/index.html) para python 3. Sendo facilmente instalado por meio do `pip install crcmod`.

## Estrutura do pacote de dados
Para implementar a fragmentação e o CRC, a estrutura de pacote de dados teve o Head e o Payload remodelados da seguinte forma:

#### Head:
```python
def StructHead(self):
  self.headStart = 0xFF
  self.headStruct = Struct("start" / Int16ub, "size" / Int16ub, "totalDataSize"  / Int16ub,
                          "typeCommand" / Int8ub, "crc_head" / Int8ub, "crc_payload" / Int8ub)
```

**Campos novos** :new:
1. `totalDateSize`: representa o tamanho total do dado a ser transferido.
1. `crc_head`: representa o CRC do Head calculado com CRC-8
1. `crc_payload`: representa o CRC do Head calculado com CRC-8

#### Payload:
Os dados do payload agora tem um um limite de tamanho de 2035 bytes, para que o pacote todo tenha 2048 bytes, visto que o *Head* tem 9 bytes e o EOP 4 bytes.

## Tempo de Timeout
O tempo de Timeout para a conexão foi estipulado para ser de 2 segundos, para estabilizar a interação entre envio e recebimento, dado que cada ponta da conexâo tem seu delay de execusão

## Melhorias e futuras implementações
1. Go-N-Back ou Selective Repeat ARQ
1. Implementação Própria do CRC, com mudança para CRC-16
1. Timeout variando de acordo com o tempo médio de resposta entre os nós durante o Handshake e transmissão de dados.
