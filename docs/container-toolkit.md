# Instalação do NVIDIA Container Toolkit

Este guia descreve como configurar o NVIDIA Container Toolkit, que permite que containers Docker utilizem GPUs NVIDIA.


## Passo 1: Adicionar chave GPG e repositório da NVIDIA

Adicione a chave GPG da NVIDIA e configure o repositório do NVIDIA Container Toolkit:

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
```
```bash
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

## Passo 2: Atualizar lista de pacotes

Atualize a lista de pacotes para incluir o repositório NVIDIA:

```bash
sudo apt-get update
```

## Passo 3: Instalar o NVIDIA Container Toolkit

Agora, instale o NVIDIA Container Toolkit:

```bash
sudo apt-get install -y nvidia-container-toolkit
```

## Passo 4: Configurar o Docker para utilizar o runtime NVIDIA
Adicione a seguinte configuração no arquivo /etc/docker/daemon.json para definir o runtime padrão como nvidia:

```json
{
    "default-runtime": "nvidia",
    "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    }
}
```

> Nota: Caso o arquivo /etc/docker/daemon.json já exista e contenha outras configurações, integre a nova configuração, garantindo a validade da sintaxe JSON.

## Passo 5: Reiniciar o Docker

Reinicie o serviço Docker para aplicar as mudanças:

```bash
sudo systemctl restart docker
```

## Passo 6: Verificar a configuração da GPU

Para verificar se o Docker está configurado corretamente para usar GPUs, execute o seguinte comando:

```bash
docker run --rm --gpus all nvidia/cuda:12.4.1-cudnn-devel-ubuntu20.04 nvidia-smi
```

Se tudo estiver configurado corretamente, você verá a saída do comando nvidia-smi, mostrando as GPUs disponíveis no sistema.


## Referências:

[Instalação do NVIDIA Container Toolkit](https://medium.com/@u.mele.coding/a-beginners-guide-to-nvidia-container-toolkit-on-docker-92b645f92006)