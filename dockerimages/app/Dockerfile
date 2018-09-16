FROM python:3.6-slim
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "./manage.py", "runserver", "0.0.0.0:8000" ]

EXPOSE 8000
