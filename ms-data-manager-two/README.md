# **Inventory MS Core Nessus**
![Supported Python versions](https://img.shields.io/badge/Python-3.9-orange.svg)
MS Core Nessus, gets asset information using Nessus API connector, updates information every 4 hours, listens to kafka topics and executes tasks.
## **Libraries**
* fastapi==0.78
* pydantic==1.9.0
* uvicorn==0.17.6
* fastapi-utils==0.2.1
* pymongo==4.1.1
* numpy==1.21.6
* xlsxwriter==3.0.3
* requests==2.27.1
* motor==3.0.0
* pydantic_vault==0.7.1
* aiokafka==0.7.2
* python-telegram-handler==2.2.1
## **Deploy Services**
docker build -t  .

#### Comandos Docker Compose
- Levantar servicios
  - ```docker-compose up -d```
- Bajar servicios
  - ```docker-compose down```
- Listar servicios
  - ```docker-compose ps```
- Verificar logs de un servicio
  - ```docker-compose logs -f nombre-servicio```
#### Comando para eliminar todas las imagenes en none
- ```docker images -a | grep "none" | awk '{print $3}' | xargs docker rmi -f```
## **Prepare Local Environment**
- Crear entorno virtual
  - ```python3 -m venv venv```
- Activar entorno virtual
  - ```source venv/bin/activate```
- Instalar librerías
  - ```pip3 install -r requirements-dev.txt```
- Levantar proyecto
  - ```python3 main.py```
- Desactivar el entorno virtual
  - ```deactivate```

## Maintainer

William Ayala
wayala@telconet.ec
