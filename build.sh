#!/bin/bash

# Atualiza os pacotes
apt-get update && apt-get install -y wget unzip

# Instala o Google Chrome
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./google-chrome-stable_current_amd64.deb

# Confirma a instalação
google-chrome --version
