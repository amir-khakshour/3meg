FROM python:3.7
ENV PYTHONUNBUFFERED 1

LABEL maintainer="khakshour.amir@gmail.com" \
    com.example.version="0.0.1-alpha"  \
    com.example.release-date="2020-02-11"

WORKDIR /app/

COPY . /app
RUN make install
COPY scripts/dev/run_uwsgi.sh scripts/dev/run_beat.sh /

