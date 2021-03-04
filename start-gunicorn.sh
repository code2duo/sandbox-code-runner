#!/bin/bash

gunicorn --bind :8000 --workers 1 --threads 8 --timeout 0 code_runner.wsgi:application &
