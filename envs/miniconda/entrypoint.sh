#!/bin/bash
set -e

# Definir o caminho onde o Miniconda será instalado
MINICONDA_DIR="$HOME/miniconda"
MINICONDA_INSTALLER="Miniconda3-latest-Linux-x86_64.sh"
MINICONDA_URL="https://repo.anaconda.com/miniconda/$MINICONDA_INSTALLER"

# Verificar se o Miniconda já está instalado
if [ -d "$MINICONDA_DIR" ]; then
    echo "Miniconda já está instalado em $MINICONDA_DIR."
else
    echo "Miniconda não encontrado. Instalando Miniconda..."

    # Baixar o instalador do Miniconda
    wget $MINICONDA_URL -O /tmp/$MINICONDA_INSTALLER

    # Tornar o instalador executável
    chmod +x /tmp/$MINICONDA_INSTALLER

    # Executar o instalador no modo silencioso
    /tmp/$MINICONDA_INSTALLER -b -p $MINICONDA_DIR

    # Remover o instalador
    rm /tmp/$MINICONDA_INSTALLER

    echo "Miniconda instalado com sucesso em $MINICONDA_DIR."

    # Adicionar Miniconda ao PATH, se ainda não estiver
    export PATH="$MINICONDA_DIR/bin:$PATH"

    # Inicializar o Conda
    $MINICONDA_DIR/bin/conda init

    # Adicionar ao .profile
    echo ". ~/.bashrc" >> ~/.profile

    $MINICONDA_DIR/bin/conda create -y -n tf python=3.11
    $MINICONDA_DIR/bin/conda run -n tf pip install tensorflow[and-cuda]
    echo "Ambiente tensorflow instalado"

    $MINICONDA_DIR/bin/conda create -y -n pytorch python=3.11
    $MINICONDA_DIR/bin/conda run -n tf pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
    echo "Ambiente pytorch instalado"

fi

# Cria a pasta necessária para o SSH
mkdir -p /var/run/sshd

# Executa o daemon SSH
/usr/sbin/sshd -D &

echo "Ambiente pronto e ssh ativo"

# Executar um shell interativo com o ambiente Miniconda ativo
exec bash