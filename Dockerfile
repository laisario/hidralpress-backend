FROM python:3.11
WORKDIR /hidralpress
ADD . /hidralpress/
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]