FROM python:3.11.0

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
COPY ./entrypoint.sh entrypoint.sh

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/opt/app/entrypoint.sh"]
