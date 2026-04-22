FROM python:3.11-slim
ENV PYTHONPATH="/app:/app/api_tester"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest allure-pytest
RUN pip uninstall -y bcrypt
RUN pip install bcrypt==4.0.1

# копируем весь проект
COPY . .

# запускаем тесты из папки tests
WORKDIR /app/tests

CMD ["pytest", "--alluredir=/results"]
