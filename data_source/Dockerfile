# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Set the timezone
RUN apt-get update && apt-get install -y tzdata
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir fastapi uvicorn[standard] confluent-kafka aiohttp

# Run app.py when the container launches, replace main with your filename without the .py extension
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "39000"]