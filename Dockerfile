# Используем легковесный образ Python на основе Alpine
FROM python:3.10-alpine

# Устанавливаем системные зависимости
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

# Создаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY pharmacy_metrics.py .
COPY apo_list.yml .

# Открываем порт для Prometheus
EXPOSE 8008

# Запускаем приложение
CMD ["python", "pharmacy_metrics.py"]
