# Adiciona a imagem padrão
FROM pytorch/pytorch:2.4.1-cuda12.4-cudnn9-runtime

# Instala programas necessarios
RUN apt-get update && apt-get install -y  openssh-server git sudo

# Expor a porta 22 para SSH
EXPOSE 22

# Copia o script de entrada
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Define o script como ponto de entrada
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]