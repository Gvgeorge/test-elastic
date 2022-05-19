FROM python:3.9-alpine3.15

WORKDIR /testlastic

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./app ./app

CMD ["python", "app/main.py"]