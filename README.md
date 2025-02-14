# Docker-Lab
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![Static Badge](https://img.shields.io/badge/version-1.2-blue)
![Static Badge](https://img.shields.io/badge/tests-passed-green)

Bem-vindo ao *Docker-Lab!* Este repositório contém imagens e utilitários para criar e gerenciar ambientes de desenvolvimento para deep learning, automatizando a configuração de um Docker Compose personalizado para cada usuário do laboratório. O objetivo do projeto é fornecer ambientes dockerizados isolados, com acesso controlado às GPUs da máquina host, sem impactar as configurações de outros usuários ou os recursos compartilhados.

## Funcionalidades
 - Ambientes Isolados: Criação de ambientes de desenvolvimento dedicados para cada usuário com uso exclusivo de GPUs disponíveis.
 - Automatização: Geração automática de arquivos docker-compose.yml personalizados para cada usuário.
 - Gerenciamento de Recursos: Controle de acesso às GPUs da máquina host sem interferir nas configurações ou recursos de outros containers em execução.
 - Imagens Otimizadas: Imagens Docker customizadas com suporte a frameworks de deep learning como TensorFlow e PyTorch, além de drivers NVIDIA configurados.

## Requisitos
Antes de utilizar o Docker-Lab, certifique-se de que sua máquina atende aos seguintes requisitos:

- [NVIDIA Drivers para uso de GPUs](./docs/nvidia-driver.md)
- [Docker instalado](./docs/docker-install.md)
- [NVIDIA Container Toolkit instalado para acesso a GPUs](./docs/container-toolkit.md)

## Instalação

### 1. Clonando o repositório

Primeiro, clone o repositório para sua máquina local:
```
git clone https://github.com/viplabufma/Docker-Lab
cd Docker-Lab
```

### 2. Instalação de dependências
O projeto utiliza algumas dependências Python para automatizar a criação do arquivo docker-compose.yaml. Para instalar essas dependências, utilize o comando abaixo:

```
pip install -r requirements.txt
```

### 3. Configuração

#### 3.1. Arquivo de ambiente
Altere o arquivo .env na raiz do projeto com as seguintes configurações:

```
MEMORY_LIMIT=4g
CPU_LIMIT=6.0
ENV_PATH=/home/username/labenvs/
```

Você pode ajustar o limite de memória de acordo com a capacidade do seu sistema, o *env path* é a pasta em que esta os dados das pastas de usuarios dos ambientes, separadas por nome de usuario.

#### 3.2. Configurando usuários
As informações dos usuários e seus ambientes são definidas em um arquivo users.json. Exemplo de estrutura:

```json
[
  {
    "user": "usuario1",
    "password": "senhaSegura",
    "device_id": "0",
    "env": "tf-2.10",
    "ssh-port": 2020
  },
  {
    "user": "usuario2",
    "password": "outraSenhaSegura",
    "device_id": "1",
    "env": "pytorch",
    "ssh-port": 2021
  }
]
```

#### 3.3. Criando imagem e compose 

Nesta etapa, as imagens Docker para cada ambiente (por exemplo, TensorFlow, PyTorch, etc.) serão construídas e um arquivo docker-compose.yml personalizado será gerado para iniciar os containers conforme a configuração dos usuários. O processo é automatizado através de um script Python incluso no projeto.


1. Construção das Imagens:

O script lê o arquivo users.json e, com base na propriedade env de cada usuário, constrói as imagens correspondentes utilizando os Dockerfiles presentes em `./envs/<env>`.

2. Geração do Docker Compose:

Em seguida, o script utiliza as configurações do arquivo .env e users.json para criar um arquivo docker-compose.yml personalizado. Esse arquivo incluirá, para cada usuário, as seguintes configurações:

- Nome do container
- Imagem a ser utilizada
- Mapeamento de portas (porta SSH)
- Variáveis de ambiente (como USER_NAME e PASSWORD)
- Volumes mapeados (diretórios de dados e backup)

O script é executado no seguinte comando:

```bash
python create-compose.py
```

#### 3.4. Criando Containers

Após a geração do arquivo docker-compose.yml, os containers podem ser criados e iniciados utilizando o Docker Compose. Para isso, execute o comando:

```bash
docker-compose create
```

### 4. Gestão de Ambientes

Após a criação dos containers, eles são instanciados, porém não iniciados automaticamente. Essa abordagem permite que os administradores ou usuários com acesso à interface gráfica gerenciem o ciclo de vida dos containers conforme necessário.

## Personalização
Se você precisa de frameworks adicionais ou configurações personalizadas, o Docker-Lab permite modificar os Dockerfiles, é possivel criar novos ambientes adicionando pastas ao `./envs/`.

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests para melhorias, correções de bugs ou novas funcionalidades.
