FROM ubuntu:18.04
WORKDIR /app
COPY requirements.txt .
RUN apt update && apt install -y python3-pip libmysqlclient-dev python-dev
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["sh", "-c", "gunicorn main:app -b 0.0.0.0:8000"]