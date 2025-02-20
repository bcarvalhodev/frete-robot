#!/bin/bash

# Atualiza os pacotes
apt-get update && apt-get install -y wget unzip

# Baixar o Chrome Portable
wget https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.76/linux64/chrome-linux64.zip

# Descompactar o Chrome
unzip chrome-linux64.zip

# Adicionar o Chrome no PATH (caso necessário)
export PATH=$PATH:/chrome-linux64

# Instalar as dependências
pip install -r requirements.txt

# Confirma a instalação do Google Chrome
./chrome-linux64/google-chrome-stable --version
