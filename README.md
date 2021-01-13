# MTM2020 JOB SUBMITTER

Este repositório possui os códigos fonte para implementar meu projeto final do concurso da IBM Master the Mainframe.

O projeto consiste em um IoT que lista os JCL no mainframe e o usuário pode selecionar qual JOB irá submenter.

Após a submissão do JOB o MTM2020 JOB SUBMITTER irá exibir no display o JOB ID e irá aguardar a conclusão da execução, após o término teremos três cenários:
* Caso a execução terminar com sucesso, irá exibir no display uma mensagem de felicitação e acenderá o um LED verde.
* Caso a execução terminar com sucesso, porém, houver algum warning, irá exibir no display o retun code e acenderá o LED amarelo.
* Caso a execução terminar com erro, será exibido no display o código de erro ou a mensagem de erro e acenderá o LED vermelho.

Foi utilizado para esse projeto os seguintes itens:
- Um single-board computer Orange PI Zero rodando a versão do Linux Armbian.
- Cartão de memória de 2Gb para a armazenar o sistema operacional.
- Um display LCD 2004.
- 3 Push buttons.
- 3 LEDs (Vermelho, Amarelo, Verde).
- 3 Resistores de 10k
- 3 Resistores de 220R
- 1 Protoboard.
- Jumpers para protoboard (Fios).



#Installing NodeJs

sudo apt install nodejs

#Installing NPM

sudo apt install npm

#Installing Zowe CLI

sudo npm config set @brightside:registry https://api.bintray.com/npm/ca/brightside

sudo npm install -g @brightside/core@lts-incremental

Ignore as mensagens de erros

#Install Python PIP

sudo apt-get install python3-pip

#habilitando interface i2c no Armbian

sudo armbian-config

System >> Hardware >> i2c0 (checked with space) >> Save >> Back >> reboot

#habilitando interface i2c no Raspbian

sudo raspi-config

Interfacing Options >> I2C >> Yes >> OK	 >> Finish 

#Installing smbus

sudo apt-get install python3-smbus

#Install GPIO library for Python

sudo pip3 install --upgrade OPi.GPIO

# Clone scripts of the MTM Job Submmiter

git clone https://github.com/maxwellwolf/mtm2020jobsubmitter.git
cd mtm2020jobsubmitter

#Alterando as variáveis de dataset e conexão

Caso queira apontar para outra biblioteca de JCL e/ou alterar os parâmentros de conexão é necessário editar as seguintes variáveis do script mtmjobsubmitter.py:

# Variaveis de conexão
path = "Z00209.JCL" # Biblioteca com as fontes JCL
ipHost = "192.86.32.153" # IP do ZOSMF
portHost = "10443" # Porta do ZOSMF
user = "z00209" # ID de usuário
passwd = "fruit102" # Senha de usuário
  
#Incluindo script para executar no boot

sudo sed -i '13 isudo python3 /home/mtm/mtm2020jobsubmitter/mtmjobsubmitter.py' /etc/rc.local
