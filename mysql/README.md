# MySQL Docker Setup

This README describes how to setup a MySQL server using Docker.

## Prerequisites

- Docker is installed on your system

## Steps to Setup MySQL in Docker

### Step 1: Pull the MySQL Docker Image

Pull the MySQL Docker image from Docker Hub using the following command in your terminal:

```bash
docker pull mysql
```

### Step 2: Run the MySQL Container

Next, run the MySQL container with a command like this:

```bash
docker run --name coin-mysql -e MYSQL_ROOT_PASSWORD=mysqlisgood -p 3306:3306 -d mysql
```

In this command:

- `--name some-mysql` sets the name of the container to "some-mysql". You can choose any name you like.
- `-e MYSQL_ROOT_PASSWORD=mysqlisgood` sets the root password.
- `-p 3306:3306` maps port 3306 in the container to port 3306 on your host machine. This is the default MySQL port.
- `-d mysql` specifies that you want to run the container in the background and print the container ID, using the "mysql" image.

### Step 3: Connect to the MySQL Server in the Container

Once the MySQL container is running, you can connect to the MySQL server using the following command:

```bash
docker exec -it some-mysql mysql -uroot -p
```

It will prompt you for the root password you set when you started the container.

