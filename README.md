# Docker-Lab

Bem-vindo ao *Docker-Lab!* Este repositório contém imagens e utilitários para criar e gerenciar ambientes de desenvolvimento para deep learning, automatizando a configuração de um Docker Compose personalizado para cada usuário do laboratório. O objetivo do projeto é fornecer ambientes dockerizados isolados, com acesso controlado às GPUs da máquina host, sem impactar as configurações de outros usuários ou os recursos compartilhados.

## Funcionalidades
 - Ambientes Isolados: Criação de ambientes de desenvolvimento dedicados para cada usuário com uso exclusivo de GPUs disponíveis.
 - Automatização: Geração automática de arquivos docker-compose.yml personalizados para cada usuário.
 - Gerenciamento de Recursos: Controle de acesso às GPUs da máquina host sem interferir nas configurações ou recursos de outros containers em execução.
 - Imagens Otimizadas: Imagens Docker customizadas com suporte a frameworks de deep learning como TensorFlow e PyTorch, além de drivers NVIDIA configurados.

## Requisitos
Antes de utilizar o Docker-Lab, certifique-se de que sua máquina atende aos seguintes requisitos:

- Docker instalado
- NVIDIA Drivers para uso de GPUs
- NVIDIA Container Toolkit instalado para acesso a GPUs

## Instalação

Clone o repositório:
```
git clone https://github.com/viplabufma/Docker-Lab
cd Docker-Lab
```

## Personalização
Se você precisa de frameworks adicionais ou configurações personalizadas, o Docker-Lab permite modificar os Dockerfiles e ajustar os parâmetros de configuração no arquivo docker-compose.yml.

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests para melhorias, correções de bugs ou novas funcionalidades.