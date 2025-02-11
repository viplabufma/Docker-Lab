import os
import json
import docker
import argparse

from utils import *

from dotenv import load_dotenv

def parse_args():
    parser = argparse.ArgumentParser(
        description="Script for building images and setting up containers."
    )
    parser.add_argument(
        "--force-build",
        action="store_true",
        default=False,
        help="Force the images to be rebuilt. Default: False."
    )
    parser.add_argument(
        "--users",
        type=str,
        default="./users.json",
        help="Path to the JSON file containing user information. Default: ./users.json."
    )
    parser.add_argument(
        "--env-path",
        type=str,
        default="./envs/",
        help="Path to the environments for image builds. Default: ./envs/."
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    load_dotenv()
    client = docker.from_env()

    # Create images based on the provided environment path and force-build option
    create_images(client, envs_path=args.env_path, force_build=args.force_build)

    # Get the base path for the home directory of the current user
    base_home_path = os.getenv('ENV_PATH', os.path.expanduser("~"))

    # Load user data from the JSON file provided as an argument
    user_data = load_users_data(args.users)

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
