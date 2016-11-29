#!/bin/bash

cd "/home/admin-s/envs/weasy/"
source bin/activate

cd "/home/admin-s/weasy-server/"
# gunicorn --bind 0.0.0.0:5001 wsgi:app
python wsgi.py
