FROM python:3.8.10-slim-buster

RUN mkdir /beaures_query

WORKDIR /beaures_query

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY beaures_query.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP beaures_query.py
EXPOSE 80

ENTRYPOINT ["/beaures_query/boot.sh"]
