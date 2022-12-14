# set base image (host OS)
FROM python:latest

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

COPY main.py .
COPY .env .
ENV TZ="Europe/Amsterdam"
CMD ["python", "./main.py"]