FROM python:3.11.9-alpine3.19

WORKDIR /srv

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY frankenstein.txt .

COPY run.py .

CMD python run.py
