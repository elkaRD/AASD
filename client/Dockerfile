FROM python:3.9.7-slim

WORKDIR /usr/app/

COPY requirements.txt ./

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . ./

ENTRYPOINT [ "python", "main.py" ]
