#!/bin/bash

make build
uwsgi --ini uwsgi.ini
