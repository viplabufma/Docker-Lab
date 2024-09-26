# Instalação do NVIDIA Container Toolkit

Este guia descreve como configurar o NVIDIA Container Toolkit, que permite que containers Docker utilizem GPUs NVIDIA.


## Passo 1: Adicionar chave GPG e repositório da NVIDIA

Adicione a chave GPG da NVIDIA e configure o repositório do NVIDIA Container Toolkit:

```
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

## Passo 2: Atualizar lista de pacotes

Atualize a lista de pacotes para incluir o repositório NVIDIA:

```
sudo apt-get update
```

## Passo 3: Instalar o NVIDIA Container Toolkit

Agora, instale o NVIDIA Container Toolkit:

```
sudo apt-get install -y nvidia-container-toolkit
```

## Passo 4: Reiniciar o Docker

Reinicie o serviço Docker para aplicar as mudanças:

```
sudo systemctl restart docker
```

## Passo 5: Verificar a configuração da GPU

Para verificar se o Docker está configurado corretamente para usar GPUs, execute o seguinte comando:

```
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

Se tudo estiver configurado corretamente, você verá a saída do comando nvidia-smi, mostrando as GPUs disponíveis no sistema.


## Referências:

[Instalação do NVIDIA Container Toolkit](https://medium.com/@u.mele.coding/a-beginners-guide-to-nvidia-container-toolkit-on-docker-92b645f92006)