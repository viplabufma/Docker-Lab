# Adiciona a imagem padrão
FROM pytorch/pytorch:2.4.1-cuda12.4-cudnn9-runtime

# Definir argumentos para o nome do usuário e senha
ARG USER_NAME=myuser
ARG PASSWORD=mysecretpassword

# Instalar OpenSSH e outras dependências
RUN apt-get update && apt-get install -y openssh-server sudo && \
    mkdir /var/run/sshd && \
    # Gerar as chaves de host SSH se elas não existirem
    [ -f /etc/ssh/ssh_host_rsa_key ] || ssh-keygen -t rsa -q -f /etc/ssh/ssh_host_rsa_key -N '' && \
    [ -f /etc/ssh/ssh_host_ecdsa_key ] || ssh-keygen -t ecdsa -q -f /etc/ssh/ssh_host_ecdsa_key -N '' && \
    [ -f /etc/ssh/ssh_host_ed25519_key ] || ssh-keygen -t ed25519 -q -f /etc/ssh/ssh_host_ed25519_key -N '' && \
    # Adicionar o usuário com o nome passado como argumento e criar home
    useradd -m -s /bin/bash ${USER_NAME} && \
    # Adicionar o usuário ao grupo sudo para permissões elevadas (opcional)
    usermod -aG sudo ${USER_NAME} && \
    # Definir a senha do usuário utilizando o argumento passado
    echo "${USER_NAME}:${PASSWORD}" | chpasswd && \
    # Permitir login de root sem senha e habilitar autenticação por senha
    sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    # Ajustar permissões para garantir que o novo usuário tenha acesso às chaves SSH
    chown -R ${USER_NAME}:${USER_NAME} /etc/ssh

# Expor a porta 22 para SSH
EXPOSE 22

# Definir o diretório de trabalho
WORKDIR /home/${USER_NAME} 

# Definir o usuário padrão para o container
USER ${USER_NAME}

# Comando para iniciar o SSH e garantir a geração de chaves de host
CMD ["/bin/bash", "-c", "mkdir -p /var/run/sshd && /usr/sbin/sshd -D"]