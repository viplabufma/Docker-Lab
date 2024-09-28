compose_header = '''version: '3.8'

services:''';

compose_service = '''
  {USER}-{ENV}-gpu-{DEVICE_ID}:
    build:
      context: ./envs/{ENV}
      dockerfile: Dockerfile
      args:
        USER_NAME: {USER}  # Passando o argumento USER_NAME
        PASSWORD: {PASSWORD}  # Passando o argumento PASSWORD
    tty: true
    ports:
      - {PORT}:22
    volumes:
      - {USER_HOME}:/home/{USER}
      - /backup:/backup
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
''';
