#!/bin/bash

# Atualiza os pacotes
apt-get update && apt-get install -y wget unzip

# Baixar o Chrome
wget -q https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.76/linux64/chrome-linux64.zip

# Descompactar o Chrome
unzip chrome-linux64.zip

# Tornar o Chrome executável
chmod +x chrome-linux64/chrome

# Verificar se o Chrome foi instalado corretamente
./chrome-linux64/chrome --version

# Instalar as dependências
pip install -r requirements.txt
