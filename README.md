# Docker-Lab

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
```

Você pode ajustar o limite de memória de acordo com a capacidade do seu sistema.

#### 3.2. Configurando usuários
As informações dos usuários e seus ambientes são definidas em um arquivo users.json. Exemplo de estrutura:

```json
[
  {
    "user": "usuario1",
    "password": "senhaSegura",
    "device_id": "0",
    "env": "tensorflow"
  },
  {
    "user": "usuario2",
    "password": "outraSenhaSegura",
    "device_id": "1",
    "env": "pytorch"
  }
]
```

## Personalização
Se você precisa de frameworks adicionais ou configurações personalizadas, o Docker-Lab permite modificar os Dockerfiles e ajustar os parâmetros de configuração no arquivo docker-compose.yml.

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests para melhorias, correções de bugs ou novas funcionalidades.