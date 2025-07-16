# pharmacy_exporter

Имеется target_list.yml файл со списком url.
```
- targets:
  - https://0007-target.ru/target0007/hs/exch_pharmacies/ping
  - https://0014-target.ru/target0014/hs/exch_pharmacies/ping
  - https://0009-target.ru/target0009/hs/exch_pharmacies/ping
```

Если выполнить 
```
curl  -u USER:PASSWORD https://0007-target.ru/target0007/hs/exch_pharmacies/ping 
```

Получим  json вида
```
{

"status": "Connected",

"metrics": [

{

"name": "Чек.РМК",

"value": 11.05083809

},

{

"name": "Обработка.СборкаИУпаковкаЗаказовКлиентов.РаскладкаЗаказовКлиентовВПакеты.ЗавершитьСканированиеНаСервере",

"value": 0.73525

},

{

"name": "Обработка.ПриемкаУпакованныхЗаказовКлиентовИзРЦ.ОбработатьШКЗаказаСоСклада",

"value": "no data"

},

{

"name": "Обработка.ТСД.РаскладкаЗаказовПоЯчейкамНовоеРазмещение.ЗавершитьСканированиеНаСервере",

"value": 0.782

},

{

"name": "Обработка.СборкаЗаказаКлиентаНаКассе.СобратьЗаказНаКассеНаСервере",

"value": "no data"

},

{

"name": "Обработка.ОрдернаяПриемкаМДЛП.СформироватьПриемныеОрдераНаСервере",

"value": 8.10033333

},

{

"name": "РегламентноеЗадание.ОтложеннаяФискализацияЗаказовКлиентовВСервисе",

"value": 8.25966667

}

]

```

Программа будет обходить все адреса из target_list.yml и для каждого получать json, из которого дальше будет извлекать имя метрики и её значение. к примеру  "name": "Чек.РМК",
"value": 11.05083809

А потом это всё оформлять как метрики для Prometheus.

## Как это работает:
Загрузка целей: Программа читает список URL-адресов из YAML-файла (target_list.yml).

## Сбор метрик: 
### Для каждого URL:

Извлекает идентификатор аптеки из URL

Выполняет аутентифицированный запрос к API

Обрабатывает ответ

## Обработка данных:

Для каждой метрики в JSON-ответе создается соответствующая метрика Prometheus

Значения преобразуются в числа ("no data" становится -1)

Добавляются лейблы: pharmacy_id и metric_name

## Экспорт метрик:

pharmacy_metric: основная метрика со значениями

pharmacy_up: статус доступности API (1 = доступно, 0 = недоступно)

Периодичность: Данные обновляются каждые 30 секунд

## Требования:
1. Установить необходимые зависимости:

```
pip install pyyaml requests prometheus_client
```

2. Создайте файл target_list.yml в том же каталоге с содержимым:

```
targets:
  - https://0007-target.ru/target0007/hs/exch_pharmacies/ping
  - https://0014-target.int.eapteka.ru/target0014/hs/exch_pharmacies/ping
  - и т.д.
```

## Использование:
1. Запустите скрипт:

```
python pharmacy_exporter.py
```

2. Настройте джобу Prometheus для сбора метрик с этого экспортера:

```
scrape_configs:
  - job_name: 'pharmacy_metrics'
    static_configs:
      - targets: ['localhost:8008']
```

## Пример получаемых метрик в Prometheus:
```
\# HELP pharmacy_metric Metric from pharmacy API

\# TYPE pharmacy_metric gauge

pharmacy_metric{metric_name="Чек.РМК",pharmacy_id="0007"} 11.05083809

pharmacy_metric{metric_name="Обработка.СборкаИУпаковкаЗаказовКлиентов.РаскладкаЗаказовКлиентовВПакеты.ЗавершитьСканированиеНаСервере",pharmacy_id="0007"} 0.73525

pharmacy_metric{metric_name="Обработка.ПриемкаУпакованныхЗаказовКлиентовИзРЦ.ОбработатьШКЗаказаСоСклада",pharmacy_id="0007"} -1

...

\# HELP pharmacy_up Availability of pharmacy API

\# TYPE pharmacy_up gauge

pharmacy_up{pharmacy_id="0007"} 1

pharmacy_up{pharmacy_id="0014"} 0
```



    
