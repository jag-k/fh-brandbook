command = "/var/www/mp_zspo/env/bin/gunicorn"
pythonpath = "/var/www/mp_zspo"
bind = "127.0.0.1:8000"
workers = 3
user = "bitrix"
limit_request_fields = 32000
limit_request_field_size = 0
