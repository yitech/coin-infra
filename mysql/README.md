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
docker run --rm --name coin-mysql  -v $(pwd)/mysql-data:/var/lib/mysql  -e MYSQL_ROOT_PASSWORD=mysqlisgood -p 3306:3306 -d mysql
```

In this command:

- `--name some-mysql` sets the name of the container to "some-mysql". You can choose any name you like.
- `-e MYSQL_ROOT_PASSWORD=mysqlisgood` sets the root password.
- `$(pwd)/mysql-data` specifies a directory named mysql-data in your current directory ($(pwd) expands to the current directory's path).
- `/var/lib/mysql` is the path inside the Docker container where MySQL stores its data.
- `-p 3306:3306` maps port 3306 in the container to port 3306 on your host machine. This is the default MySQL port.
- `-d mysql` specifies that you want to run the container in the background and print the container ID, using the "mysql" image.

### Step 3: Connect to the MySQL Server in the Container

Once the MySQL container is running, you can connect to the MySQL server using the following command:

```bash
docker exec -it coin-mysql mysql -uroot -p
```

It will prompt you for the root password you set when you started the container.

## Create Orderbook

### Step 1: Create a New Database

```sql
CREATE DATABASE coin_project;
```

### Step 2: Use the New Database

Select the database you just created with the USE command:

```sql
USE coin_project;
```

### Step 3: Create `OrderBookRequest` and `OrderBookEntry` Table

Create the `OrderBookRequest` table with the following command:

```sql
CREATE TABLE OrderBookRequest (
    request_id INT AUTO_INCREMENT,
    request_time TIMESTAMP,
    response_time TIMESTAMP,
    exchange VARCHAR(255),
    symbol VARCHAR(255),
    PRIMARY KEY (request_id)
);
```

### Step 4: Create the `OrderBookEntry` Table 

Create the `OrderBookEntry` table with the following command:

```sql
CREATE TABLE OrderBookEntry (
    entry_id INT AUTO_INCREMENT,
    request_id INT,
    price DECIMAL(14, 4),
    size DECIMAL(14, 4),
    type ENUM('ask', 'bid'),
    PRIMARY KEY (entry_id),
    FOREIGN KEY (request_id) REFERENCES OrderBookRequest(request_id)
);
```
