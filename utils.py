import os
import json

from dotenv import load_dotenv
from compose_templates import compose_header, compose_service

load_dotenv()

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


def create_service(service_param, base_home_path):
    # Create the home directory for the user if it doesn't exist
    user_home = get_user_path_home(service_param, base_home_path)
    
    service = compose_service.format(
                USER=service_param['user'],
                DEVICE_ID=service_param['device_id'],
                ENV=service_param['env'],
                PASSWORD=service_param['password'],
                PORT=service_param['port'],
                USER_HOME=user_home,
                MEMORY_LIMIT = os.getenv('MEMORY_LIMIT', '4g'),
                CPU_LIMIT = os.getenv('CPU_LIMIT', '6.0'))
    
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