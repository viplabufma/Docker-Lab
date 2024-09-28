import os
import json


from utils import generate_docker_compose, create_services, load_users_data, create_and_check_path, write_docker_compose

from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    # Get the base path for the home directory of the current user
    base_home_path = os.getenv('ENV_PATH', os.path.expanduser("~"))

    # Load user data from users.json
    user_data = load_users_data()

    # Check users permission in volume
    create_and_check_path(user_data, base_home_path)

    # Create services of compose
    services = create_services(user_data, base_home_path)

    # Generate the docker-compose string
    docker_compose = generate_docker_compose(services)

    # Write the docker-compose.yaml file
    write_docker_compose(docker_compose)
