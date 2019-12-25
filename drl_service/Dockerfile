FROM python:3.7-alpine
COPY requirements.txt /
RUN pip3.7 install -r /requirements.txt
COPY . /app
WORKDIR /app
CMD ["python", "api.py"]

