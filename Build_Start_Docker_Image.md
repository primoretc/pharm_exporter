1. Создайте структуру файлов:

pharmacy-exporter/

├── Dockerfile

├── requirements.txt

├── pharmacy_metrics.py

└── apo_list.yml

2. Соберите Docker-образ:

```
docker build -t pharmacy-exporter:latest .
```

3. Запустите контейнер:

```
docker run -d \
  -p 8008:8008 \
  -e SCRAPE_INTERVAL=60 \  # Установить интервал 60 секунд
  -v $(pwd)/target_list.yml:/target/target_list.yml \
  --name pharmacy-exporter \
  pharmacy-exporter:latest
```



4. При локальном запуске минуя Docker 
### Для Linux/macOS
```
SCRAPE_INTERVAL=15 python pharmacy_metrics.py
```
### Для Windows PowerShell

```
$env:SCRAPE_INTERVAL = 15
python pharmacy_metrics.py
```
