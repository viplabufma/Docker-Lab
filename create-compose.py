import os

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
    '''.format(USER=service_param['user'],
               DEVICE_ID=service_param['device_id'],
               FRAMEWORK=service_param['framework'],
               PASSWORD=service_param['password'],
               PORT=service_param['port'],
               USER_HOME=user_home)
    
    return service


if __name__ == "__main__":
    # Get the base path for the home directory of the current user
    current_user_home = os.path.expanduser("~")

    # Define users, passwords, device_ids, and the framework for each user
    users = ['user']
    passwords = ['userP@ssw0r']
    device_ids = ['0'] 
    frameworks = ['tensorflow']  

    services = []

    # Create a service for each user with their respective framework and device
    for i, user in enumerate(users):
        service_params = {
            'user': user,
            'password': passwords[i],
            'device_id': device_ids[i],
            'framework': frameworks[i],
            'port': 2020 + i  # Increment port number for each user
        }
        service = create_service(service_params, current_user_home)
        services.append(service)

    generate_docker_compose(services)
