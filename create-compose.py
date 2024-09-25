import os
import json

from dotenv import load_dotenv  # Importa a função para carregar o .env

# Carregar variáveis do arquivo .env
load_dotenv()

def generate_docker_compose(services, filename='docker-compose.yaml'):
    header = '''version: '3.8'

services:
    '''

    with open(filename, 'w') as file:
        file.write(header)

        for s in services:
            file.write(s)


def create_service(service_param, base_home_path):
    # Create the home directory for the user if it doesn't exist
    user_home = os.path.join(base_home_path,'volumes', service_param['user'])
    if not os.path.exists(user_home):
        os.makedirs(user_home)
    
    service = '''
  {USER}-{FRAMEWORK}-gpu-{DEVICE_ID}:
    build:
      context: ./{FRAMEWORK}
      dockerfile: Dockerfile
      args:
        USER_NAME: {USER}  # Passando o argumento USER_NAME
        PASSWORD: {PASSWORD}  # Passando o argumento PASSWORD
    tty: true
    ports:
      - {PORT}:22
    volumes:
      - /home/{USER}:/home/{USER}
      - /backup:/backup
    deploy:
      resources:
        reservations:
          devices:
          - driver: nvidia
            device_ids: ['{DEVICE_ID}']
            capabilities: [gpu]
        limits:
          memory: {MEMORY_LIMIT}
    '''.format(USER=service_param['user'],
               DEVICE_ID=service_param['device_id'],
               FRAMEWORK=service_param['framework'],
               PASSWORD=service_param['password'],
               PORT=service_param['port'],
               USER_HOME=user_home,
               MEMORY_LIMIT = os.getenv('MEMORY_LIMIT', '4g'))
    
    return service


if __name__ == "__main__":
    # Get the base path for the home directory of the current user
    current_user_home = os.path.expanduser("~")

    # Load user data from users.json
    with open('users.json', 'r') as f:
        user_data = json.load(f)

    services = []

    # Create a service for each user defined in the JSON file
    for i, user_info in enumerate(user_data):
        service_params = {
            'user': user_info['user'],
            'password': user_info['password'],
            'device_id': user_info['device_id'],
            'framework': user_info['framework'],
            'port': 2020 + i  # Increment port number for each user
        }
        service = create_service(service_params, current_user_home)
        services.append(service)

    # Generate the docker-compose.yaml file
    generate_docker_compose(services)
