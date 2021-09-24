FROM python:3.6-slim

WORKDIR /githoster-app

COPY app/ app/

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /githoster/app/src

RUN export FLASK_APP=modules && export FLASK_DEBUG=1
RUN export FLASK_DEBUG=1

RUN flask db init
RUN flask db migrate -m "Users table." 
RUN flask db upgrade

WORKDIR /githoster/app

EXPOSE 5000

CMD [ "flask", "./src/" ]