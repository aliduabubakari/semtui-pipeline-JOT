FROM python:3.8-slim

WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y git && apt-get clean

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt


COPY extension.py extension.py

CMD ["python", "extension.py"]
