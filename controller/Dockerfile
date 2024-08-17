FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY ../utils.py utils.py

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# sleep 10 seconds to wait for worker contaienrs to start

ENTRYPOINT ["sh", "-c", "sleep 10 && python -u app.py"]