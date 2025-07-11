# 📊 Tinkoff Bond Order Book Collector

Этот проект собирает данные по стаканам (Order Book) облигаций с помощью [Tinkoff Invest API](https://tinkoff.github.io/investAPI/) и сохраняет их в `.csv` файлы по 1000 записей в каждом.

## 📦 Структура

- `main.py` — основной скрипт
- `requirements.txt` — зависимости
- `Dockerfile` — описание сборки Docker-контейнера
- `data/` — папка для сохранения CSV-файлов (создаётся автоматически)

## 🚀 Запуск через Docker

### 1. Клонируйте или скопируйте проект

```bash
git clone https://github.com/yourname/tinkoff-bond-collector.git
cd tinkoff-bond-collector
```

### 2. Поместите ваш Tinkoff API токен в main.py
```python
TOKEN = "ВАШ_ТОКЕН_СЮДА"
```
### 3. Соберите Docker-образ
```bash
docker build -t tinkoff-stream .
```
### 4. Запустите приложение
```bash
docker run --rm -v "./data:/app/data" tinkoff-stream
```
После запуска в папке data/ будут появляться CSV-файлы с данными стаканов по указанным облигациям.

## ⚙️ Конфигурация
Список обрабатываемых тикеров находится в main.py, в переменной tickers:

```python
tickers = ['RU000A10BBW8', 'RU000A105QX1', ...]
```

## 📁 Пример выходных данных
CSV-файлы содержат поля:

- ticker

- time

- ask

- ask_vol

- bid

- bid_vol