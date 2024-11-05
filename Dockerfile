FROM python:3.11
WORKDIR /hidralpress
ADD . /hidralpress/
RUN apt update
RUN apt install -y lsyncd lua5.3 liblua5.3-dev
RUN rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
COPY lsyncd.conf.lua /etc/lsyncd/lsyncd.conf.lua
COPY start.sh start.sh
RUN chmod +x start.sh
EXPOSE 8000
CMD ["./start.sh"]