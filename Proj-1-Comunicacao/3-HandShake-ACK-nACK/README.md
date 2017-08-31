# Camada Física - Projeto 1 - COM-Handshake
Leonardo Medeiros e Martim Ferrera José

Nessa etapa do projeto, foi implementado de forma incremental um protocolo de handshake na camada de enlace que garante ao *client* que dados só serão trafegados na rede quando o *server* estiver habilitado para receber. Além disso, um protocolo de reconhecimento (ACK e NACK) foi implementado para que o *client* tenha conhecimento do status da recepção do pacote pelo *server*, caso uma falha for detectada, ele reenvia o pacote.

## Funcionamento do Handshake
O handshake foi implementado na camada *enlace* por meio de duas funções, a *connect()* para o **Client** e *bind()* para o **Server**, que funcionam como uma Máquina de estados, que avaliam os dados que estão recebendo, por meio de funcões como *getCommandType()* e *getPacketType()*.


### Handshake
Para estabelecer uma conexão segura com o *Server*, o *Client* envia um pacote comando SYN para o *Server*, que deve responder durante um tempo hábil se ele recebeu este "pedido" de Sincronização. Caso ele receba, ele deve responder (enviar) com um pacote comando ACK, monstrando reconhecimento positivo do SYN e logo depois deve enviar um SYN para firmar a conexão por sua parte. O Client ao receber este ACK + SYN, deve responder ACK para confirmar a conexão por sua parte também. Com a conexão estabelecida de forma segura, o *Client* pode enviar os pacotes de dados. Caso uma das partes responde com nAck, o handshake se reinicia. O funcionamento do handshake é ilustrado no diagrama a seguir:

![Diagrama do Handshake](doc/diagrama_handshake.png)

Os pacotes de comandos foram implementados da seguinte forma:
- Head: headStart (16 bits), size (16 bits), typeCommand (8 bits)
- Payload: *Não contém payload* -> Head size = 0
- EOP: 4 constantes (8 bits, 8 bits, 8 bits, 8 bits)

Os tipos de pacotes de comandos foram decididos da seguinte forma:
- SYN: Pacote de sincronismo (0x10)
- ACK: Pacote de reconhecimento positivo (0x11)
- nACK: Pacote de reconhecimento negativo (0x12)

Por exemplo, o pacote nACK ficaria da seguinte maneira:

---
Head: *\x00\xff\x00\x00\x12*
Payload: 
EOP: *\x01\x02\x03\x04*
---


### Integridade dos pacotes
Para verificar a integridade dos pacotes, o Server realiza 



# Requisitos

Requisitos de projeto :

1. Handshake (3Way)
    - *client* envia **SYN**, *server* responde com **ACK** + **SYN**, *client* responde com **ACK**.
    - Deve implementar ao menos os seguintes pacotes de comando (na interface enlace):
        - **SYN**  : Pacote de sincronismo 
        - **ACK**  : Pacote de reconhecimento positivo
        - **NACK** : Pacote de reconhecimento negativo
    1. Client :
        - Só pode enviar pacotes após handshake com Server
        - Deve possuir timeout para o handshake 
            - por exemplo, se o server não responder ao primeiro SYN deve enviar outro depois de *n* segundos.
    1. Server :
        - Deve aguardar pela inicialização 
        - Deve responder ao *Client* pelo pedido de inicialização.
1. Reconhecimento do pacote :
    - Após handshake o *Server* deve enviar um pacote de **ACK** ou **nACK** ao *Client* indicado o status da recepção do pacote.
    1. Client :
        - Deve enviar o pacote e aguardar pelo **ACK** ou **NACK**.
            - Caso receba um **NACK** deve reenviar o pacote.
            - Caso receba um **ACK** deve considerar o envio como positivo.
    1. Server :
        - Seve receber um pacote e verificar sua integridade.
            - Caso detecte uma anomalia, enviar um **NACK** e aguardar por novo pacote.
            - Caso receba o pacote de forma integra, enviar um **ACK** e salvar os dados.
1. Software
    - Logs em toda a etapa de Handshake (exibir no terminal o que está acontecendo).
    - Logs com relação ao ACK e nACK do pacote.

1. Documentação
    - Descrever o handshake implementado.
    - Descrever os pacotes (SYN,ACK,NACK).
        - diagrama dos pacotes.
    - Diagrame o envio de pacotes em como uma máquina de estados.
    - Diagrame a recepção de pacotes como uma máquina de estados.
    - Descrever o tempo de timeout utilizado (e o porque desse valor).
    - Como diferencia pacotes de comando (SYN,ACK,NACK) de pacote de dados ?
    
## Itens extras

1. Implementar o FIN (final de comunicação)
1. Inserir CheckSum no HEAD e Payload para detecção de anomalias nos pacotes

## Validação

- Inicializar o Client e não conectar o Server. Nenhuma imagem deve ser enviada.
- Após algum tempo inicializar o Server, deve acontecer o handshake e a transferência deve ser executada.
- Durante a transmissão, desconectar o fio que transmite dados entre Client e Server
    - Server deve responder com nACK
    - Client deve retransmitir o pacote.


## Rubricas

| Nota máxima | Descritivo                                                |
|-------------|-----------------------------------------------------------|
| A           | - Entregue no prazo                                       |
|             | - Implementado extras                                     |
| B           | - Entregue no prazo                                       |
|             | - Implementado requisitos necessários                     |
| C           | - Entregue fora do prazo                                  |
|             | - Implementando requisitos necessários                    |
| D           | - Nem todos os requisitos necessários foram implementados |
| I           | - Não entregue                                            |



