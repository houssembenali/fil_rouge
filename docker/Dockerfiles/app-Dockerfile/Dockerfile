FROM python:alpine

WORKDIR /githoster-app

COPY /docker/webapp/src/* app/


COPY /docker/webapp/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN export FLASK_APP=modules && export FLASK_DEBUG=1
RUN export FLASK_DEBUG=1

RUN flask db init
RUN flask db migrate -m "Users table." 
RUN flask db upgrade


EXPOSE 5000

CMD [ "flask", "./app/" ]