FROM python:3.7
ENV PYTHONUNBUFFERED 1

LABEL maintainer="khakshour.amir@gmail.com" \
    com.example.version="0.0.1-alpha"  \
    com.example.release-date="2020-02-11"

WORKDIR /app/

RUN groupadd -r django && useradd -r -g django django
COPY . /app
RUN chown -R django /app
RUN make install

USER django
COPY scripts/dev/run_uwsgi.sh scripts/dev/run_beat.sh /

