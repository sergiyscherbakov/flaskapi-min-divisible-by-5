# FastAPI - Пошук мінімального елемента кратного 5

Веб-додаток на FastAPI для пошуку мінімального елемента кратного 5 з використанням MongoDB.

## Опис проекту

Додаток дозволяє:
- Зберігати числа в MongoDB
- Знаходити мінімальний елемент кратний 5
- Переглядати всі збережені числа
- Очищати базу даних

## Технології

- **FastAPI** - веб-фреймворк
- **MongoDB** - база даних
- **Jinja2** - шаблонізатор
- **Bootstrap 5** - UI фреймворк

## Встановлення

1. Клонуйте репозиторій:
```bash
git clone https://github.com/sergiyscherbakov/flaskapi.git
cd flaskapi
```

2. Встановіть залежності:
```bash
pip install fastapi uvicorn pymongo jinja2
```

3. Запустіть MongoDB сервер:
```bash
mongod
```

4. Запустіть додаток:
```bash
python main.py
```

Додаток буде доступний за адресою: http://127.0.0.1:8000

## Структура проекту

```
flaskapi/
├── main.py              # Основний FastAPI додаток
├── templates/
│   └── index.html       # HTML шаблон з Bootstrap
└── README.md
```

## API Endpoints

- `GET /` - Головна сторінка
- `POST /add_numbers` - Додати числа в базу даних
- `GET /find_min_divisible_by_5` - Знайти мінімальний елемент кратний 5
- `GET /get_all_numbers` - Отримати всі числа
- `DELETE /clear_numbers` - Очистити базу даних

## MongoDB - Команди для перевірки БД

### Базові команди

Запустити MongoDB shell:
```bash
mongosh
```

Показати всі бази даних:
```javascript
show dbs
```

Перейти до бази numbers_db:
```javascript
use numbers_db
```

Показати всі колекції:
```javascript
show collections
```

Вийти з MongoDB shell:
```javascript
exit
```

### Робота з даними

Показати всі числа:
```javascript
db.numbers.find()
```

Показати тільки значення (без _id):
```javascript
db.numbers.find({}, {_id: 0, value: 1})
```

Підрахувати кількість документів:
```javascript
db.numbers.countDocuments()
```

Знайти числа кратні 5:
```javascript
db.numbers.find({value: {$mod: [5, 0]}})
```

Знайти мінімальне число кратне 5:
```javascript
db.numbers.find({value: {$mod: [5, 0]}}).sort({value: 1}).limit(1)
```

Знайти максимальне число:
```javascript
db.numbers.find().sort({value: -1}).limit(1)
```

Очистити колекцію:
```javascript
db.numbers.deleteMany({})
```

Видалити конкретне число (наприклад, 25):
```javascript
db.numbers.deleteOne({value: 25})
```

### Додаткові корисні команди

Показати статистику колекції:
```javascript
db.numbers.stats()
```

Знайти числа більші за 50:
```javascript
db.numbers.find({value: {$gt: 50}})
```

Знайти числа в діапазоні (наприклад, від 10 до 50):
```javascript
db.numbers.find({value: {$gte: 10, $lte: 50}})
```

Підрахувати кількість чисел кратних 5:
```javascript
db.numbers.countDocuments({value: {$mod: [5, 0]}})
```

## Налаштування MongoDB

База даних: `numbers_db`
Колекція: `numbers`
Порт: `27017` (за замовчуванням)

## Як використовувати додаток

1. Відкрийте браузер: http://127.0.0.1:8000
2. Натисніть кнопку "Випадкове заповнення" або введіть числа вручну через кому
3. Натисніть "Зберегти в базу даних"
4. Натисніть "Знайти мінімальний елемент кратний 5"
5. Результат буде відображено на сторінці

## Примітки

- MongoDB повинен бути запущений перед стартом додатка
- За замовчуванням MongoDB створює папку `C:\data\db` для зберігання даних
- Якщо сервер MongoDB не запускається, спробуйте видалити `C:\data\db` та створити заново
