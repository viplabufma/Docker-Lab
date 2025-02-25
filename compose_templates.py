compose_header = '''
version: '3.8'

services:
networks:
  {NETWORK_NAME}:
    driver: {NETWORK_DRIVER}
''';

compose_service = '''
  {USER}-{ENV}-gpu-{DEVICE_ID}:
    tty: true
    image: dockerlab-{ENV}:latest    # Define a imagem que será usada para criar o container
    container_name: {USER}-{ENV}-gpu-{DEVICE_ID} # Define o nome do container
    environment:
      USER_NAME: {USER}       # Nome do usuário
      PASSWORD: {PASSWORD}  # Senha do usuário
    ports:
      - {PORT}:22
    volumes:
      - {USER_HOME}:/home/{USER}
      - /backup:/backup
      {CUSTOM_VOLUME}
    shm_size: {MEMORY_LIMIT}
    deploy:
      resources:
        reservations:
          devices:
          - driver: nvidia
            device_ids: ['{DEVICE_ID}']
            capabilities: [gpu]
        limits:
          memory: {MEMORY_LIMIT}
          cpus: {CPU_LIMIT}  # Limite de CPU adicionado aqui
''';
