from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pymongo import MongoClient
from typing import List, Optional

app = FastAPI(title="Пошук мінімального елемента кратного 5")

# Підключення до MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["numbers_db"]
collection = db["numbers"]

# Налаштування шаблонів
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Головна сторінка"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/add_numbers")
async def add_numbers(numbers: str = Form(...)):
    """Додати числа в базу даних"""
    try:
        # Парсинг чисел з рядка
        num_list = [int(x.strip()) for x in numbers.split(",") if x.strip()]

        if not num_list:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Не введено жодного числа"}
            )

        # Видалення старих даних
        collection.delete_many({})

        # Додавання нових чисел
        documents = [{"value": num} for num in num_list]
        collection.insert_many(documents)

        return JSONResponse(content={
            "success": True,
            "message": f"Додано {len(num_list)} чисел до бази даних",
            "numbers": num_list
        })
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "Помилка: введіть числа через кому"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Помилка: {str(e)}"}
        )

@app.get("/find_min_divisible_by_5")
async def find_min_divisible_by_5():
    """Знайти мінімальний елемент кратний 5"""
    try:
        # Отримання всіх чисел з бази
        all_numbers = list(collection.find({}, {"_id": 0, "value": 1}))

        if not all_numbers:
            return JSONResponse(content={
                "success": False,
                "message": "База даних порожня. Спочатку додайте числа."
            })

        numbers = [doc["value"] for doc in all_numbers]

        # Пошук чисел кратних 5
        divisible_by_5 = [num for num in numbers if num % 5 == 0]

        if not divisible_by_5:
            return JSONResponse(content={
                "success": True,
                "message": "Не знайдено чисел кратних 5",
                "all_numbers": numbers,
                "divisible_by_5": [],
                "min_value": None
            })

        min_value = min(divisible_by_5)

        return JSONResponse(content={
            "success": True,
            "message": f"Знайдено мінімальний елемент кратний 5: {min_value}",
            "all_numbers": numbers,
            "divisible_by_5": divisible_by_5,
            "min_value": min_value
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Помилка: {str(e)}"}
        )

@app.get("/get_all_numbers")
async def get_all_numbers():
    """Отримати всі числа з бази даних"""
    try:
        all_numbers = list(collection.find({}, {"_id": 0, "value": 1}))
        numbers = [doc["value"] for doc in all_numbers]

        return JSONResponse(content={
            "success": True,
            "numbers": numbers,
            "count": len(numbers)
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Помилка: {str(e)}"}
        )

@app.delete("/clear_numbers")
async def clear_numbers():
    """Очистити всі числа з бази даних"""
    try:
        result = collection.delete_many({})
        return JSONResponse(content={
            "success": True,
            "message": f"Видалено {result.deleted_count} чисел з бази даних"
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Помилка: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
