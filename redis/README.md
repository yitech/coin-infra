# Redis-Docker README

This README will guide you through the process of setting up a Redis service using Docker. 

## Pre-Requisites

1. Install Docker: Docker must be installed on your machine. Please visit the [Docker Getting Started Guide](https://www.docker.com/get-started) to download Docker and install it on your system if you haven't done so already.

## Instructions

1. **Pull Redis Docker Image**

In your terminal, execute the following command to pull the latest Redis image from Docker Hub.

 ```bash
 docker pull redis
 ```

2. **Run Redis Container**

Next, you can start a Redis instance with the following command:

 ```bash
 docker run --name some-redis -d redis
 ```
Here, `--name coin-redis` names the container "some-redis" and `-d` detaches the container to run in the background.

To start Redis on a specific port, use the `-p` flag:

 ```bash
 docker run --name coin-redis -d -p 6379:6379 redis
 ```

In this case, Redis is available on `localhost:6379`.

3. **Interact with Redis**

You can interact with Redis using the Redis CLI in another Docker container:

 ```bash
 docker run -it --network some-network --rm redis redis-cli -h some-redis
 ```

You can replace `--network some-network` with `--link some-redis:redis` in non-Swarm mode.

## Data Persistence

If you want data to persist across container restarts or deletions, use Docker volumes:

```bash
docker run --name some-redis -d redis redis-server --appendonly yes
```

If you wish to store the data in a specific directory on your host system, use the `-v` option:

```bash
docker run --name coin-redis -v $(pwd)/redis/data:/data -d redis redis-server --appendonly yes
```

In this case, `$(pwd)/redis/data` is the directory on your host system, and `/data` is the path in the Docker container where Redis stores its data.

## Custom Configuration

If you wish to use a custom Redis configuration, you can create a custom `redis.conf` file and mount it into the docker container:

```bash
docker run --name coin-redis -v /my/own/redis.conf:/usr/local/etc/redis/redis.conf -d redis redis-server /usr/local/etc/redis/redis.conf
```

Here, `/my/own/redis.conf` is the path to your custom configuration file on your host machine.

## Stopping the Redis Service

To stop the Redis service, you can use Docker's `stop` command:

```bash
docker stop coin-redis
```

## Removing the Redis Container

If you want to completely remove the container (and all associated data if not persisted), you can use Docker's `rm` command:

```bash
docker rm coin-redis
```

Remember to replace `coin-redis` with the name of your Redis container.

## Conclusion

That's it! You should now be able to run a Redis service inside a Docker container. This is especially handy for development environments, as it allows you to quickly start and stop services as needed. 

For more information about Redis and Docker, you can check out the official documentation for both [Redis](https://redis.io/documentation) and [Docker](https://docs.docker.com/).