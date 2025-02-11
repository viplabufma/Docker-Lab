#!/bin/bash
set -e

# Inicializa o Conda
/opt/conda/bin/conda init bash

# Adicionar ao .profile
echo ". ~/.bashrc" >> ~/.profile

# Cria a pasta necessária para o SSH
mkdir -p /var/run/sshd

# Executa o daemon SSH
/usr/sbin/sshd -D &

# Inicia um shell interativo do Bash
exec /usr/bin/bash -l