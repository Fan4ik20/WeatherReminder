#Pull the base image
FROM python:3.10-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

#upgrading pip for python
RUN python -m pip install --upgrade pip

#copying requirements.txt file
COPY ./requirements.txt /app/requirements.txt

#install those requirements before copying the project
RUN pip install -r /app/requirements.txt

#copy the project
COPY . .

#run gunicorn. here pdfconverter is the project name
CMD gunicorn -b 0.0.0.0:$PORT DjangoWeatherReminder.wsgi:application
