# MTM2020 JOB SUBMITTER

Este repositório possui os códigos fonte para implementar meu projeto final do concurso da IBM Master the Mainframe.

O projeto consiste em um IoT que lista os JCL no mainframe e o usuário poderá selecionar qual JOB irá submeter.

Após a submissão do JOB o MTM2020 JOB SUBMITTER irá exibir no display o JOB ID e aguardará a conclusão da execução, após o término teremos três cenários:
* Caso a execução terminar com sucesso, irá exibir no display uma mensagem de felicitação e acenderá o um LED verde.
* Caso a execução terminar com sucesso, porém, houver algum warning, irá exibir no display o retun code e acenderá o LED amarelo.
* Caso a execução terminar com erro, será exibido no display o código de erro ou a mensagem de erro e acenderá o LED vermelho.

Foi utilizado para esse projeto os seguintes itens:
- Um single-board computer Orange PI Zero rodando a versão do Linux Armbian.
- Cartão de memória de 2Gb para a armazenar o sistema operacional.
- Um display LCD 2004 com módulo i2c.
- 3 Push buttons.
- 3 LEDs (Vermelho, Amarelo, Verde).
- 3 Resistores de 10k
- 3 Resistores de 330R
- 1 Protoboard.
- Jumpers para protoboard (Fios).

## Esquema com as ligações dos componentes ao Orange PI Zero

Por padrão a maioria dos single-board computer disponíveis no mercado possuem o mesmo layout de pinos.
No caso do esquema abaixo estamos utilizando os pinos ímpares, sendo o pino 1 o primeiro da direita para esquerda de cima para baixo.

![Schema](https://github.com/maxwellwolf/mtm2020jobsubmitter/blob/master/Pinouts.jpg?raw=true)

## Preparando o ambiente para execução

Para baixar a versão da imagem do Armbian para sua placa basta acessar o link de download do [Armbian](https://www.armbian.com/download/).

Não irei entrar em detalhes sobre a instalação da imagem do Armbian no cartão de memória pois existem diversos tutoriais na internet.

Prorem, como sou muito bom (Rsrs),  vou deixar esse [link](https://www.albertogonzalez.net/how-to-install-armbian-debian-on-an-orange-pi-zero/) que mostra a instalação bem detalhada do Armbian para o Orange PI Zero, mas as instruções servem para qualquer outra placa.

Após realizar todas as ligações na placa, o Armibian instalado no SD, logado ao terminal via SSH e com acesso a internet,  vamos preparar o Armbiam para executar nosso script em python.

Essas instruções e as pinagens acima servirá para qualquer computer-board compatível com Armbiam.


### Instalando o NodeJs

`sudo apt install nodejs`

Caso a instalação tenha ocorrido com sucesso ao emitir o comando `nodejs -v` irá mostar a versão do Node

### Instalando o NPM

`sudo apt install npm`

Caso a instalação tenha ocorrido com sucesso ao emitir o comando `npm -v` irá mostrar a versão do NPM

### Instalando o Zowe CLI

Essa API é o que faz tudo acontecer, será através dela que iremos interagir com o mainframe.

`sudo npm config set @brightside:registry https://api.bintray.com/npm/ca/brightside`

`sudo npm install -g @brightside/core@lts-incremental`

Ignore as mensagens de erros

Se ao emitir o comando `zowe -V` exibir a versão do ZOWE, ocorreu tudo bem, podemos seguir em frente.

### Instalando o Python PIP

`sudo apt-get install python3-pip`

### Habilitando interface i2c no Armbian

Por padrão, a interface i2c do Armbian está desabilitada, para habilitar usaremos a GUI de configuração do SO.

`sudo armbian-config`

System >> Hardware >> i2c0 (Habilita com a tecla espaço) >> Save >> Back >> reboot

Obs. Para o correto funcionamento do script é importante que seja habilitado a interface i2c0.

### Instalando a biblioteca smbus

A biblioteca python3-smbus é responsável por gerir a comunicação entre a interface i2c.

`sudo apt-get install python3-smbus`

### Instalando a biblioteca GPIO para Python

A biblioteca python OPi.GPIO permite acessar e controlar as interfaces GPIO Orange PI Zero.
Essa biblioteca permite um mapeamento pelo número do pino, e não pelo número da porta, permitindo que o mesmo código seja executado em diferentes single-board computer de mercado sem a necessidade de alteração no código.

`sudo pip3 install --upgrade OPi.GPIO`

### Clonando o repositório com os scripts do MTM2020 Job Submmiter

Agora vamos tranferir para o Armbian os arquivos do nosso projeto.

`git clone https://github.com/maxwellwolf/mtm2020jobsubmitter.git`

`cd mtm2020jobsubmitter`

### Alterando as variáveis de dataset e conexão

Caso queira apontar para outra biblioteca de JCL e/ou alterar os parâmetros de conexão é necessário editar as seguintes variáveis do script mtmjobsubmitter.py:

```
path = "Z00000.JCL"      # Biblioteca com as fontes JCL
ipHost = "192.86.32.153" # IP do ZOSMF
portHost = "10443"       # Porta do ZOSMF
user = "z00000"          # ID de usuário
passwd = "fruit102"      # Senha de usuário
```  

### Incluindo script para executar no boot

`sudo sed -i '13 isudo python3 /home/mtm/mtm2020jobsubmitter/mtmjobsubmitter.py' /etc/rc.local`

## GO, GO, GO!

Se toda a instalação ocorreu bem e foram feitas as ligações corretamente podemos executar nosso script com o comando:

`sudo python3 mtmjobsubmitter.py`

Ou se preferir, reinicie o Armbiam que o script executará assim que o sistema terminar de carregar.

`sudo reboot`

Após inicializar o script você verá na primeira linha do display "MTM20 JOB SUBMITTER!" e o primeiro JCL da lista na segunda linha.

Para navegar entre os JCL aperte os botões UP e DOWN, ao escolher o JOB a ser executado, pressione o botão SUB para submeter o JOB e agora é só aguardar o término da execução.

Segue o vídeo do projeto em funcionamento:

[![MTM20 JOB SUBMITTER](https://i9.ytimg.com/vi/gtbkg5on7vc/mq3.jpg?sqp=CLC7_P8F&rs=AOn4CLBy4wr7uzF5hR5rV8VenkttQ2eOQQ)](https://youtu.be/gtbkg5on7vc)
