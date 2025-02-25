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

# Função para extrair a porta do arquivo
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
# Configuração do SSH
# =============================================
echo "Configuring SSH..."
mkdir -p /var/run/sshd

# Gerar chaves SSH de host
echo "Generating SSH host keys..."
for key_type in rsa ecdsa ed25519; do
    key_file="/etc/ssh/ssh_host_${key_type}_key"
    [ -f "$key_file" ] || ssh-keygen -t $key_type -q -f "$key_file" -N ''
done

# =============================================
# Configuração do usuário
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
# Aplicar configurações do SSH
# =============================================
echo "Updating SSH configuration..."
SSHD_CONFIG="/etc/ssh/sshd_config"

# Atualizar porta (comentada ou não)
sed -i "/^#*Port\s\+/c\Port $SSH_PORT" "$SSHD_CONFIG"

# Demais configurações
sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' "$SSHD_CONFIG"
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' "$SSHD_CONFIG"

# =============================================
# Ajustes de permissões
# =============================================
echo "Adjusting permissions..."
chown -R "$USER_NAME":"$USER_NAME" /etc/ssh
chown -R "$USER_NAME":"$USER_NAME" "/home/$USER_NAME"

# =============================================
# Configuração do ambiente Conda
# =============================================
echo "Initializing Conda..."
/opt/conda/bin/conda init bash
echo ". ~/.bashrc" >> ~/.profile

# =============================================
# Inicialização dos serviços
# =============================================
echo "Starting SSH daemon on port $SSH_PORT..."
exec /usr/sbin/sshd -D -e "$@"
