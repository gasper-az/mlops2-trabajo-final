# MLOps 2 - Trabajo Final 

## Componentes

- [MLFlow](./mlflow/): tracking server. Permite loguear modelos y metricas de estos.
  - Implementa `Minio` para almacenar datos.
  - Implementa `PostgreSQL` para almacenar datos.
- [Trainer](./trainer/): entrena un modelo LogisticRegression utilizando el [Wine Quality Dataset](https://www.kaggle.com/datasets/yasserh/wine-quality-dataset) y lo loguea en MLFlow.
- [gRPC server](./grpc-server/): servidor de inferencia, que expone un endpoint para realizar predicciones mediante el modelo anterior.
  - Es importante remarcar que en la carpeta [proto](./proto/) se encuentra la definicion de este servicio.
  - A partir de este [proto](./proto/) se crea los archivos [protogen](./protogen/), mas precisamente, los archivos de python.
    - **IMPORTANTE**: no modificar estos archivos.
  - Esto se hace mediante el comando definido en el [makefile](./makefile). Para ello, ejecutar `make proto PYTHON=python`.
- [REST API](./http-api/): HTTP REST API que tiene un endpoint mediante el cual se hacen predicciones.
- [GraphQL API](./graphql-api/): API GraphQL (Strawberry) que expone una mutation `predict` cargando el modelo desde MLflow (puerto 8090).
- Kafka: se utiliza como broker de mensajes. El servidor de inferencia envia resultados de predicciones en este broker.
- [Spark Drift Detector](./spark-drift-detector/): Permite detectar DRIFT o corrimiento de las distribuciones de los datos.
  - Por el momento, solo las loguea por pantalla.
  - Implementa Spark, procesando en tiempo real los resultados de las inferencias enviadas en un broker de Kafka desde el servidor de inferencia.
- [Carpeta reference](./reference/): contiene un archivo con el formato de las estadisticas/metricas de referencia de cada feature utilizada. Se obtuvo desde mlflow.
- [Scripts - generate_traffic](./scripts/generate_traffic.py): permite generar trafico *falso* a fin de probar el funcionamiento del detector de drift de Spark.

### Como ejecutar la aplicacion?

**Prerequisito**

1. Crear stubs de gRPC:
   1. `make proto`
      1. Alternativamente `make proto PYTHON=python` o `make proto PYTHON=python3` para indicar el interprete de python a utilizar.

**Mediante Docker compose**

1. `docker compose up -d`
   1. Alternativa: `docker compose up --build -d` para hacer build de la aplicacion
2. `docker compose down -v` para eliminar los containers + volumenes.

**Mediante makefile**

1. `make up`
   1. Alternativa: `make up-build` para hacer build de la aplicacion
2. `make down` para eliminar los containers + volumenes.

### Como hacer llamados a la REST API?

Documentación interactiva (Swagger UI): [http://localhost:8080/docs](http://localhost:8080/docs)

```bash
curl http://localhost:8080/health
```

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-type: application/json" \
  -d '{
    "alcohol": 13.2,
    "malic_acid": 1.7,
    "ash": 2.3,
    "alcalinity_of_ash": 15.6,
    "magnesium": 98,
    "total_phenols": 2.8,
    "flavanoids": 3.0,
    "nonflavanoid_phenols": 0.3, 
    "proanthocyanins": 1.9,
    "color_intensity": 5.5,
    "hue": 1.0,
    "od280_od315": 3.2,
    "proline": 520
  }'
```

### Como hacer llamados a la GraphQL API?

Documentación interactiva (GraphiQL): [http://localhost:8090/graphql](http://localhost:8090/graphql)

Health:

```bash
curl http://localhost:8090/health
```

Mutation `predict` con `curl` (los campos del input van en **camelCase** en GraphQL):

```bash
curl -s http://localhost:8090/graphql \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"mutation { predict(features: { alcohol: 13.2, malicAcid: 1.7, ash: 2.3, alcalinityOfAsh: 15.6, magnesium: 98, totalPhenols: 2.8, flavanoids: 3.0, nonflavanoidPhenols: 0.3, proanthocyanins: 1.9, colorIntensity: 5.5, hue: 1.0, od280Od315: 3.2, proline: 520 }) { predictedClass modelVersion } }\"}"
```

Misma mutation en GraphiQL:

```graphql
mutation {
  predict(
    features: {
      alcohol: 13.2
      malicAcid: 1.7
      ash: 2.3
      alcalinityOfAsh: 15.6
      magnesium: 98
      totalPhenols: 2.8
      flavanoids: 3.0
      nonflavanoidPhenols: 0.3
      proanthocyanins: 1.9
      colorIntensity: 5.5
      hue: 1.0
      od280Od315: 3.2
      proline: 520
    }
  ) {
    predictedClass
    modelVersion
  }
}
```

### Como ejecutar el Drift Detection?

**Mediante python**

Ejecutar `python scripts/generate_traffic.py` en una terminal.

**Mediante makefile**

1. `make drift-traffic`
   1. `make drift-traffic PYTHON=python` o `make drift-traffic PYTHON=python3`

**Recomendaciones**

Ejecutar en una terminal el siguiente comando para observar en tiempo real como Kafka procesa los eventos que recibe del inference server.
***NOTA***: se puede ejecutar en Linux y Windows (sacar `sudo`).

```bash
sudo docker exec -it kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic wine.inference.events
```

Para ver la deteccion de data-drift y/o data-poisoning:

```bash
sudo docker exec -it kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic wine.security.alerts
```

Para verlos desde el comienzo:

```bash
sudo docker exec -it kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic wine.security.alerts --from-beginning
```

<!-- Ejecutar en una terminal para ver los logs (por el momento, prints en pantalla) de cuando se encuentran drifts.
Tambien se recomienda ir al [sitio local de Spark](http://localhost:4040/).
***NOTA***: se puede ejecutar en Linux y Windows (sacar `sudo`).

```bash
sudo docker logs spark-drift-detector
``` -->

### Como configurar Grafana?

1. Ir al sitio http://localhost:3000
2. Hacer login con admin user.
3. Una vez hecho login, si grafana solicita cambiar la password, cambiarla o hacer skip.
4. En el panel izquierdo, ir a `Connections/Data Sources`.
5. `Add data source` y luego filtrar por `PostgreSQL`.
6. Completar con los siguientes datos;
   1. Name: cualquier nombre, como `postgresql-source`
   2. Connection:
      1. Host URL: `postgres:5432`.
      2. Database name: `mlflow`.
   3. Authentication:
      1. Username: `mlflow`.
      2. Password: `mlflow`.
      3. TLS/SSL Mode: `disabled`.
   4. Al final de la pagina, clickear `Save & test`. Esto deberia mostrar un mensaje que dice `Database connection OK`.
   5. En la URL, copiar el `UID` del dashboard. Ejemplo: `http://localhost:3000/connections/datasources/edit/***afin5lvhpbls0b***`.
7. Agregar Dashboard
   1. En el panel izquierdo, ir a `Dashboards`.
   2. `Create Dashboard`.
   3. `import`.
   4. Pegar el codigo de [security_alerts.json](./grafana/security_alerts.json).
   5. Presionar `load`.
   6. Luego, cambiar el `UID` con el correspondiente de tu data source.
   7. `Import`.

### PostgreSQL

```bash
sudo docker exec -it postgres psql -U mlflow -d mlflow
```

```bash
SELECT * from security_alerts ORDER BY timestamp DESC;
```

## Next Steps

1. Detectar data poisoning con Spark (y su logica de drift).
1. Agregar out-of-distribution detection en tiempo de inferencia.

### To organize

> **NOTE**: De aca para abajo es delirio mio. Desestimar hasta que lo organice correctamente.

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
curl http://localhost:8080/health
```

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-type: application/json" \
  -d '{
    "alcohol": 13.2,
    "malic_acid": 1.7,
    "ash": 2.3,
    "alcalinity_of_ash": 15.6,
    "magnesium": 98,
    "total_phenols": 2.8,
    "flavanoids": 3.0,
    "nonflavanoid_phenols": 0.3, 
    "proanthocyanins": 1.9,
    "color_intensity": 5.5,
    "hue": 1.0,
    "od280_od315": 3.2,
    "proline": 520
  }'
```

#### Responses

```bash
{"predicted_class":1,"model_version":"latest"}
```

#### Prueba de kafka

sudo docker exec -it kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic wine.inference.events --from-beginning

#### Kafka + Spark 

sudo docker exec -it kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic wine.inference.events

sudo docker logs spark-drift-detector