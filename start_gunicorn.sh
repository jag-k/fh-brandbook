#!/bin/bash
source /var/www/mp_zspo/env/bin/activate
gunicorn -c "/var/www/mp_zspo/gunicorn_config.py" wsgi