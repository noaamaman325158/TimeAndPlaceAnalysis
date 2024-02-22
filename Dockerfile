FROM python:3.9-slim

WORKDIR /app

COPY app/mock_sensor_api.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENV NAME World

CMD ["python", "mock_sensor_api.py"]
