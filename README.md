### To organize

#### For pyenv

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl git libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

```bash
curl https://pyenv.run | bash
```

```bash
nano ~/.bashrc
```

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi
```

```bash
source ~/.bashrc
```

```bash
pyenv install 3.11.8
```

Ejecutar alguno de estos comandos:

```bash
pyenv global 3.11.8
```

```bash
pyenv local 3.11.8
```

#### Docker compose

En Linux Mint, borrar base docker

```bash
sudo apt remove docker-compose
sudo apt remove docker docker-engine docker.io docker-compose
```

Luego ejecutar

```bash
sudo apt update
sudo apt install ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu jammy stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Instalar
```bash
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Validar versi'on (v2 o mayor).

```bash
docker compose version
```

#### Start docker

```bash
sudo systemcl start docker
```

#### Evitar usar sudo con docker

```bash
sudo usermod -aG docker $USER
```

#### Instalar

```bash
python -m pip install grpcio-tools
```

#### For makefile

> Si no tenes los `poetry.lock` en cada subproyecto, ejecuta los comandos de poetry en cada uno.

```bash
make proto PYTHON=python
make up
```

> Intentar con `sudo` en caso que `make up`  no funcione.

Alternativa:

```bash
docker compose build --no-cache
docker compose up
```

#### REST API

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-type: application/json" \
  -d '{"features":[5.1,3.5,1.4,0.2]}'
```

#### Responses

| Value | Clase |
| --- | --- |
| 0 | setosa |
| 1 | versicolor |
| 2 | virginica |
