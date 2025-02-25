#!/bin/bash
set -e

# Variáveis para o nome do usuário e senha
USER_NAME=${USER_NAME:-defaultuser}
PASSWORD=${PASSWORD:-defaultpassword}

# =============================================
# Leitura da porta do arquivo ssh_port
# =============================================
SSH_PORT_FILE="/home/$USER_NAME/ssh_port"
DEFAULT_SSH_PORT=22

get_ssh_port() {
    if [ -f "$SSH_PORT_FILE" ]; then
        grep -E "^Port [0-9]+$" "$SSH_PORT_FILE" | awk '{print $2}' || echo $DEFAULT_SSH_PORT
    else
        echo $DEFAULT_SSH_PORT
    fi
}

# Obter porta do SSH
SSH_PORT=$(get_ssh_port)
echo "Configuring SSH to use port: $SSH_PORT"

# Apagar o arquivo ssh_port após a leitura
rm -f "$SSH_PORT_FILE"

# =============================================
# Configurar o diretório para SSH
# =============================================
echo "Configuring SSH..."
mkdir -p /var/run/sshd

# =============================================
# Gerar chaves SSH de host, se não existirem
# =============================================
echo "Generating SSH host keys if they do not exist..."
[ -f /etc/ssh/ssh_host_rsa_key ]     || ssh-keygen -t rsa     -q -f /etc/ssh/ssh_host_rsa_key -N ''
[ -f /etc/ssh/ssh_host_ecdsa_key ]   || ssh-keygen -t ecdsa   -q -f /etc/ssh/ssh_host_ecdsa_key -N ''
[ -f /etc/ssh/ssh_host_ed25519_key ] || ssh-keygen -t ed25519 -q -f /etc/ssh/ssh_host_ed25519_key -N ''

# =============================================
# Criar o usuário dinamicamente, se não existir
# =============================================
if ! id "$USER_NAME" &>/dev/null; then
    echo "Creating user: $USER_NAME"
    useradd -m -s /bin/bash "$USER_NAME"
    echo "$USER_NAME:$PASSWORD" | chpasswd
    usermod -aG sudo "$USER_NAME"
else
    echo "User $USER_NAME already exists"
fi

# =============================================
# Configurar SSH para permitir login com senha e root
# =============================================
echo "Configuring SSH authentication to allow root login and password authentication..."
sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Atualizar a porta do SSH no arquivo de configuração
sed -i "/^#*Port\s\+/c\Port $SSH_PORT" /etc/ssh/sshd_config

# =============================================
# Ajustar permissões para garantir que o novo usuário tenha acesso às chaves SSH
# =============================================
echo "Adjusting SSH permissions for user $USER_NAME..."
chown -R "$USER_NAME":"$USER_NAME" /etc/ssh

# =============================================
# Ajustar permissões para o diretório home do usuário
# =============================================
echo "Setting ownership of home directory for $USER_NAME..."
chown -R "$USER_NAME":"$USER_NAME" /home/"$USER_NAME"

# =============================================
# Inicializa o Conda
# =============================================
echo "Initializing Conda..."
su - "$USER_NAME" -c '/opt/miniconda/bin/conda init bash'

# Adicionar ao .profile para carregar o bashrc
echo "Adding Conda initialization to .profile..."
echo 'eval "conda activate tf"' >> ~/.bashrc 
echo ". /home/$USER_NAME/.bashrc" >> /home/"$USER_NAME"/.profile

# =============================================
# Cria a pasta necessária para o SSH (caso não tenha sido criada anteriormente)
# =============================================
echo "Ensuring /var/run/sshd exists..."
mkdir -p /var/run/sshd

# =============================================
# Entra na pasta do usuário
# =============================================
echo "Changing to home directory of $USER_NAME..."
cd /home/"$USER_NAME"

# =============================================
# Executa o daemon SSH
# =============================================
echo "Starting SSH daemon on port $SSH_PORT..."
/usr/sbin/sshd -D &

# =============================================
# Inicia um shell interativo do Bash
# =============================================
echo "Starting interactive Bash shell..."
exec /usr/bin/bash -l
