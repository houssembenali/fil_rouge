FROM python:alpine

WORKDIR /githoster-app

COPY app/ app/


COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest
RUN pip install pytest-cov

RUN ["pytest", "-v", "--cov=app", "--junitxml=rapports/resultats.xml"]
CMD tail -f /dev/null