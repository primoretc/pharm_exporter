# Полная структура проекта:

pharmacy-exporter/

├── docker-compose.yml

├── Dockerfile

├── requirements.txt

├── pharmacy_metrics.py

└── apo_list.yml

## Как использовать:
Сборка образа (выполняется один раз или при изменениях кода):

```
docker-compose build
```

## Запуск сервиса (с интервалом по умолчанию 30 секунд):

```
docker-compose up -d
```

## Запуск с кастомным интервалом (например, 60 секунд):

```
SCRAPE_INTERVAL=60 docker-compose up -d
```

## Проверка работы:

### Проверить логи

```
docker-compose logs -f
```

### Проверить метрики

```
curl http://localhost:8008/metrics
```

## Обновление конфигурации (без перезапуска контейнера):

### Отредактируйте target_list.yml

```
vim target_list.yml
```

### Перезапустите контейнер для применения изменений

```
docker-compose restart
```

## Расширенные возможности:

Использование .env файла (для постоянных настроек):

Создайте файл .env в той же директории:

```
SCRAPE_INTERVAL=120
```
Теперь при запуске будет автоматически использоваться этот интервал:

```
docker-compose up -d
```

## Обновление кода:
 После изменения кода

```
docker-compose build
docker-compose up -d --force-recreate
```

## Масштабирование (если потребуется):

```
docker-compose up -d --scale pharmacy-exporter=3
```
