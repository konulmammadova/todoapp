FROM python:3.6

#PYTHONDONTWRITEBYTECODE means Python won’t try to write .pyc files which we also do not desire.
ENV PYTHONDONTWRITEBYTECODE 1

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /todoapp

# Set the working directory to /music_service
WORKDIR /todoapp

# Copy the current directory contents into the container at /music_service
ADD . /todoapp/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000


