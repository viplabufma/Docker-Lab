compose_header = '''
version: '3.8'

services:
''';

compose_service_header = '''
  {USER}-{ENV}-gpu-{DEVICE_ID}:
    tty: true
    image: dockerlab-{ENV}:latest    # Define a imagem que será usada para criar o container
    container_name: {USER}-{ENV}-gpu-{DEVICE_ID} # Define o nome do container
'''

compose_service_portainer_accesscontrol= '''    io.portainer.accesscontrol.teams: "{PORTAINER_ACCESSCONTROL_TEAM}" # Define o time de controle no portainer
'''

compose_service_env = '''
    environment:
      USER_NAME: {USER}       # Nome do usuário
      PASSWORD: {PASSWORD}  # Senha do usuário
'''

compose_service_env_host_net = '''
    environment:
      USER_NAME: {USER}       # Nome do usuário
      PASSWORD: {PASSWORD}  # Senha do usuário
      SSH_PORT: {PORT}  # Porta ssh
'''

compose_service_ports = '''
    ports:
      - {PORT}:22
'''

compose_service_volumes = '''
    volumes:
      - {USER_HOME}:/home/{USER}
      - /backup:/backup
'''

compose_service_resources = '''
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
    network_mode: {NETWORK_DRIVER}
'''

def build_compose_service_template(dict):
    compose_service = ""
    compose_service = compose_service + compose_service_header
    compose_service = compose_service + compose_service_portainer_accesscontrol if dict["PORTAINER_ACCESSCONTROL_TEAM"] else compose_service
    compose_service = compose_service + compose_service_env_host_net if dict['NETWORK_DRIVER'] == "host" else compose_service + compose_service_env
    compose_service = compose_service if dict['NETWORK_DRIVER'] == "host" else compose_service + compose_service_ports
    compose_service = compose_service + compose_service_volumes
    compose_service = compose_service + compose_service_resources
    return compose_service