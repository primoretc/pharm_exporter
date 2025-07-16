import yaml
import requests
import re
import os
from prometheus_client import start_http_server, Gauge
import time
from typing import List, Dict, Any, Union

# Создаем метрики Prometheus
PHARMACY_METRIC = Gauge(
    'pharmacy_metric', 
    'Metric from pharmacy API',
    ['pharmacy_id', 'metric_name']
)
PHARMACY_UP = Gauge(
    'pharmacy_up', 
    'Availability of pharmacy API',
    ['pharmacy_id']
)

def extract_pharmacy_id(url: str) -> str:
    match = re.search(r'https://(\d+)-app', url)
    if match:
        return match.group(1)
    return 'unknown'

def load_targets(filename: str) -> List[str]:
    with open(filename, 'r') as f:
        data = yaml.safe_load(f)
    
    # Обработка разных форматов YAML
    if isinstance(data, list):
        return data[0].get('targets', [])
    elif isinstance(data, dict) and 'targets' in data:
        return data['targets']
    return []

def fetch_metrics(url: str, auth: tuple) -> Union[Dict[str, Any], None]:
    try:
        response = requests.get(url, auth=auth, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return None

def process_metrics(pharmacy_id: str, metrics_data: Dict[str, Any]):
    PHARMACY_UP.labels(pharmacy_id=pharmacy_id).set(1)
    
    for metric in metrics_data.get('metrics', []):
        name = metric.get('name', 'unknown')
        value = metric.get('value', 'no data')
        
        try:
            numeric_value = float(value)
        except (ValueError, TypeError):
            numeric_value = -1
        
        PHARMACY_METRIC.labels(
            pharmacy_id=pharmacy_id,
            metric_name=name
        ).set(numeric_value)

def main():
    YAML_FILE = 'target_list.yml'
    AUTH = ('ADMIN', 'PASSWORD')
    
    # Получаем интервал из переменной окружения (по умолчанию 30 секунд)
    try:
        SCRAPE_INTERVAL = int(os.getenv('SCRAPE_INTERVAL', '30'))
    except ValueError:
        SCRAPE_INTERVAL = 30
        print("Invalid SCRAPE_INTERVAL value. Using default 30 seconds.")
    
    # Загружаем список адресов
    targets = load_targets(YAML_FILE)
    print(f"Loaded {len(targets)} targets")
    print(f"Scrape interval set to {SCRAPE_INTERVAL} seconds")
    
    # Запускаем HTTP сервер для Prometheus
    start_http_server(8008)
    print("Prometheus exporter started on port 8008")
    
    # Основной цикл сбора метрик
    while True:
        print(f"Scraping {len(targets)} pharmacies...")
        for url in targets:
            pharmacy_id = extract_pharmacy_id(url)
            print(f"Processing pharmacy {pharmacy_id}...")
            
            # Получаем данные с API
            metrics_data = fetch_metrics(url, AUTH)
            
            if metrics_data:
                # Успешный запрос
                process_metrics(pharmacy_id, metrics_data)
                metric_count = len(metrics_data.get('metrics', []))
                print(f"  Success: {metric_count} metrics updated")
            else:
                # Ошибка подключения
                PHARMACY_UP.labels(pharmacy_id=pharmacy_id).set(0)
                print("  Failed to fetch metrics")
        
        print(f"Sleeping for {SCRAPE_INTERVAL} seconds")
        time.sleep(SCRAPE_INTERVAL)

if __name__ == "__main__":
    main()
