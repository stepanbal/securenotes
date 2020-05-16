FROM python:3.8

WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY Pipfile /usr/src/app/
COPY Pipfile.lock /usr/src/app/

RUN pip install pipenv
RUN set -ex && pipenv install --deploy --system

COPY entrypoint.sh /usr/src/app/entrypoint.sh
COPY . /usr/src/app/
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
