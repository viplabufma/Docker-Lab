# Instalação do Driver NVIDIA 555 no Ubuntu

Este guia descreve como instalar o driver NVIDIA versão 555 no Ubuntu, garantindo que o sistema possa utilizar GPUs NVIDIA de forma otimizada.

## Passo 1: Verificar compatibilidade da GPU
Antes de instalar o driver, verifique qual GPU está presente no sistema:

```bash
lspci -vnn | grep VGA
```

Isso exibirá informações sobre a GPU instalada. Certifique-se de que a GPU é compatível com o driver NVIDIA 555.

## Passo 2: Atualizar lista de pacotes

Atualize o sistema para garantir que os pacotes estejam atualizados:

```
sudo apt update
sudo apt upgrade -y
```

## Passo 3: Adicionar repositório gráfico NVIDIA PPA

Adicione o repositório oficial de drivers gráficos da NVIDIA:

```
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update
```

## Passo 4: Instalar o driver NVIDIA 555

Instale o driver NVIDIA 555 com o seguinte comando:

```
sudo apt install nvidia-driver-555
```

Aguarde até que o processo de instalação seja concluído.

## Passo 5: Verificar a instalação do driver

Após a instalação, reinicie o sistema:

```
sudo reboot
```

Quando o sistema reiniciar, verifique se o driver está instalado corretamente executando o seguinte comando:

```
nvidia-smi
```

Se o driver estiver instalado corretamente, será exibida uma lista com as GPUs detectadas e suas respectivas informações.

Passo 6: Instalar o NVIDIA CUDA Toolkit (Opcional)
Se você deseja utilizar CUDA para aceleração GPU, pode instalar o toolkit correspondente:

```
sudo apt install nvidia-cuda-toolkit
```

Referência:

- [How to Install Nvidia Drivers on Ubuntu 20.04](https://phoenixnap.com/kb/install-nvidia-drivers-ubuntu)
- [NVIDIA drivers installation](https://ubuntu.com/server/docs/nvidia-drivers-installation)