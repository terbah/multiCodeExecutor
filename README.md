# Distant code executor

Author : *Aghiles Terbah*

### Starting the containers
```
docker-compose up --build
```

### Description

The project's purpose is to expose a rest api allowing clients to run code in multiple languages remotely.
When a client request arrives to the server, the request is added to a rabbitmq queue which will be treated by one the workers inside an isolated secure docker container.
