import os
import json
import docker
from typing import Dict, Any
import re
from dotenv import load_dotenv
from compose_templates import compose_header, build_compose_service_template

load_dotenv()

NETWORK_DRIVER_HOST = "host"
NETWORK_DRIVER_BRIDGE = "bridge"
DEFAULT_MEMORY_LIMIT = "4g"
DEFAULT_CPU_LIMIT = "6.0"
SSH_DEFAULT_PORT = 22

def generate_docker_compose(services):
    docker_compose = compose_header + "".join(services)
    return docker_compose

def write_docker_compose(docker_compose, filename='docker-compose.yaml'):
    with open(filename, 'w') as file:
        file.write(docker_compose)

def get_user_path_home(service_param, base_home_path):
    return os.path.join(base_home_path, 'volumes', service_param['user'])


def create_and_check_path(users_data, base_home_path):
    if not os.path.exists(base_home_path):
        os.makedirs(base_home_path)
        
    if os.access(base_home_path, os.X_OK) and os.access(base_home_path, os.W_OK) and os.access(base_home_path, os.R_OK):
        for ud in users_data:
            service_param = parse_service_params(ud)
            user_home = get_user_path_home(service_param, base_home_path)
            if not os.path.exists(user_home):
                os.makedirs(user_home)
    else:
        raise PermissionError("The user does not have permission on the chosen path")

def create_service(service_param: Dict[str, Any], base_home_path: str) -> str:
    """Cria e retorna a configuração de serviço para o Docker Compose."""
    user_home = get_user_path_home(service_param, base_home_path)
    network_driver = os.getenv('NETWORK_DRIVER', NETWORK_DRIVER_BRIDGE)

    # Formatação do template
    compose_service = build_compose_service_template({"NETWORK_DRIVER": network_driver})
    service = compose_service.format(
        USER=service_param['user'],
        DEVICE_ID=service_param['device_id'],
        ENV=service_param['env'],
        PASSWORD=service_param['password'],
        PORT=service_param['port'],
        USER_HOME=user_home,
        MEMORY_LIMIT=os.getenv('MEMORY_LIMIT', DEFAULT_MEMORY_LIMIT),
        CPU_LIMIT=os.getenv('CPU_LIMIT', DEFAULT_CPU_LIMIT),
        NETWORK_DRIVER=network_driver
    )
    return service

def load_users_data(users_file_path = 'users.json'):
    # Load user data from users.json
    user_data = None
    with open(users_file_path, 'r') as f:
        user_data = json.load(f)
    return user_data

def parse_service_params(user_info):
    return {
        'user': user_info['user'],
        'password': user_info['password'],
        'device_id': user_info['device_id'],
        'env': user_info['env'],
        'port': user_info['ssh-port']
    }


def create_services(users_data, base_home_path):
    services = []

    # Create a service for each user defined in the JSON file
    for i, user_info in enumerate(users_data):

        service_params = parse_service_params(user_info)
        
        service = create_service(service_params, base_home_path)
        
        services.append(service)

    return services

def check_ports(users_data):
    ports_userd = []
    check_passed = True

    for u in users_data:
        port = u["ssh-port"]
        if not port in ports_userd:
            ports_userd.append(port)
        else:
            check_passed = False
            raise PermissionError("the {PORT} port was requested by more than one user".format(PORT = port))
    return check_passed

def get_available_envs(path='./envs'):
    return os.listdir(path=path) 

def check_envs(users_data):
    available_envs = get_available_envs()

    for u in users_data:
        env = u["env"]
        if not env in available_envs:
            raise PermissionError("The \"{ENV}\" environment is not available in the ./envs path".format(ENV = env))

def create_images(client, envs_path = './envs', force_build = True):
    available_envs = get_available_envs()
    current_imagens = client.images.list()
    current_imagens = [x.tags for x in current_imagens]
    current_imagens = [tag for sublist in current_imagens for tag in sublist]
    

    for env in available_envs:
        image_name = "dockerlab-" + env + ":latest"
        
        if image_name in current_imagens and force_build == False:
            continue

        print("Criando imagem do ambiente:", env, "Nome:", image_name)
        try:
            image, build_logs = client.images.build(
                path=os.path.join(envs_path, env),
                tag= image_name,  # Tag para identificar a imagem
                rm=True  # Remove os containers intermediários após a build
            )

        except docker.errors.BuildError as build_error:
            print("Erro na construção da imagem:", build_error)
        except Exception as e:
            print("Erro inesperado:", e)