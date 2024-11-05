FROM python:3.11
WORKDIR /hidralpress
ADD . /hidralpress/
RUN apt update
RUN apt install -y lsyncd jq
RUN rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
COPY lsyncd.conf.lua /etc/lsyncd/lsyncd.conf.lua
COPY start.sh start.sh
COPY notify_django.sh notify_django.sh
RUN chmod +x start.sh
RUN chmod +x notify_django.sh
EXPOSE 8000
CMD ["./start.sh"]