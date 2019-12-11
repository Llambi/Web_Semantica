Dummy project to test Docker.
Instructions at [Docker Docs - Getting started with Docker](https://docs.docker.com/get-started/).

# Instructions to work with Docker, Docker-Compose and Docker-Swarm

## Images

To build the image

```bash
docker build --tag=$IMAGE_NAME .
```

To remove the image

```bash
docker image rm `docker image ls | grep $IMAGE_NAME | awk '{print $3}'`
```

## Containers

To run a container interactively with this image

```bash
docker run --publish $PORT:80 $IMAGE_NAME
```

To start a container as a daemon with this image

```bash
docker run --detach --publish $PORT:80 $IMAGE_NAME
```

To stop a container as a daemon with this image

```bash
docker container stop `docker container ls | grep $IMAGE_NAME | awk '{print $1}'`
```

## Swarm

To start the swarm

```bash
docker swarm init
```

To stop the swarm

```bash
docker swarm leave --force
```

## Stack

To deploy the stack

```bash
docker stack deploy --compose-file docker-compose.yml $STACK_NAME
```

To undeploy the stack

```bash
docker stack rm $STACK_NAME
```

## Clean

To remove all unused images, containers, volumes

```bash
docker system prune --all --force --volumes
```

To stop everything and remove all images, containers, volumes

```bash
docker stop `docker container ls --all --quiet`; docker system prune --all --force --volumes
```

## Utils

Connect toa bash to run commands

```bash
docker exec -it `docker container ls | grep $IMAGE_NAME | awk '{print $1}'` /bin/bash
```