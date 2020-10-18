FROM python:3.8
ADD requirements.txt /app/requirements.txt
ADD . /app/
WORKDIR /app/
RUN pip install -r requirements.txt