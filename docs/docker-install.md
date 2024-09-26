# Instalação do Docker no Ubuntu

Este guia descreve o processo de instalação do Docker no Ubuntu, com a adição do usuário ao grupo `docker` para permitir a execução de comandos sem `sudo`.

## Passo 1: Atualizar lista de pacotes

Antes de instalar o Docker, atualize a lista de pacotes:

```
sudo apt update
```

## Passo 2: Instalar pacotes necessários

Instale pacotes para que o APT possa usar HTTPS para a instalação do Docker:

```
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```

## Passo 3: Adicionar a chave GPG oficial do Docker

Baixe e adicione a chave GPG para o repositório oficial do Docker:

```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

## Passo 4: Adicionar o repositório Docker

Adicione o repositório oficial do Docker às fontes do APT:

```
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
```

## Passo 5: Atualizar a base de pacotes do Docker

Certifique-se de que os pacotes a serem instalados vêm do repositório Docker:

```
apt-cache policy docker-ce
```

## Passo 6: Instalar o Docker

Agora, instale o Docker:

```
sudo apt install docker-ce
```

## Passo 7: Verificar o status do Docker

Após a instalação, verifique se o Docker está ativo e em execução:

```
sudo systemctl status docker
```

## Passo 8: Executar o Docker sem sudo (Opcional)

Por padrão, o Docker exige o uso de sudo para executar seus comandos. Para evitar o uso contínuo de sudo, adicione seu usuário ao grupo docker:

```
sudo usermod -aG docker ${USER}
```

Aplique a mudança de grupo com o comando:

```
su - ${USER}
```

Verifique se o usuário foi adicionado corretamente ao grupo docker:

```
groups
```

Agora, você pode executar os comandos Docker sem sudo.


## Referências:

[Instalação do Docker no Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)