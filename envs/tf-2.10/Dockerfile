FROM nvidia/cuda:11.2.2-runtime-ubuntu20.04

# Configurar o ambiente para evitar prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# Atualizar os pacotes e instalar pacotes necessários
RUN apt-get update && \
    apt-get install -y locales tzdata openssh-server git sudo && \
    # Gerar os locales necessários
    locale-gen en_US.UTF-8 && \
    locale-gen pt_BR.UTF-8 && \
    # Atualizar o locale
    update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 && \
    # Definir o fuso horário (evitar prompt interativo)
    ln -fs /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Configurar variáveis de ambiente para o locale
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8

# Verificar se o locale foi configurado corretamente
RUN locale

# Definindo variáveis de URL e paths
ENV MINICONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-py38_23.11.0-1-Linux-x86_64.sh
ENV MINICONDA_SH=/tmp/Miniconda3-py38_23.11.0-1-Linux-x86_64.sh
ENV MINICONDA_INSTALL_PATH=/opt/conda

# Baixando, instalando e removendo o Miniconda
RUN wget $MINICONDA_URL -O $MINICONDA_SH && \
    chmod +x $MINICONDA_SH && \
    $MINICONDA_SH -b -p $MINICONDA_INSTALL_PATH && \
    rm $MINICONDA_SH && \
    echo "Miniconda instalado com sucesso"


ENV PATH="/opt/conda/bin:$PATH"

RUN conda init
RUN conda update conda
RUN conda install -y python=3.8
RUN CONDA_OVERRIDE_CUDA="11.2" conda install -y tensorflow-gpu==2.10 -c conda-forge

# Expor a porta 22 para SSH
EXPOSE 22

# # Copia o script de entrada
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# # Define o script como ponto de entrada
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]