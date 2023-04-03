FROM --platform=linux/amd64 python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
WORKDIR /app/socialnetworking
EXPOSE 8000

CMD [ "python" , "manage.py", "runserver", "0.0.0.0:8000"]