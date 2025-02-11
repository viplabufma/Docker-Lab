import os
import json


from utils import *

from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    # Get the base path for the home directory of the current user
    base_home_path = os.getenv('ENV_PATH', os.path.expanduser("~"))

    # Load user data from users.json
    user_data = load_users_data()

    # Check users permission in volume
    create_and_check_path(user_data, base_home_path)

    # Checks if there is more than one port per environment
    check_ports(user_data)

    # Check if the environment is available in the ./envs path
    check_envs(user_data)

    # Create services of compose
    services = create_services(user_data, base_home_path)

    # Generate the docker-compose string
    docker_compose = generate_docker_compose(services)

    # Write the docker-compose.yaml file
    write_docker_compose(docker_compose)
