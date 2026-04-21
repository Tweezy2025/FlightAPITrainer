FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# фиксируем рабочую версию bcrypt
RUN pip uninstall -y bcrypt
RUN pip install bcrypt==4.0.1

COPY . .

CMD ["uvicorn", "api_tester.backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
