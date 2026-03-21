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
