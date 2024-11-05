#!/bin/bash

lsyncd /etc/lsyncd/lsyncd.conf.lua&
python manage.py runserver 0.0.0.0:8000