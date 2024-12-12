from fastapi import FastAPI, Path
from typing import Annotated
from pydantic import BaseModel
from enum import Enum
from fastapi import HTTPException

# запуск сервера:
# uvicorn module_16_3:app --reload


# Создаем экземпляр приложения FastAPI

app = FastAPI()
# создаем "базу данных"

users = {'1': 'Имя: Example, возраст: 18'}

# возвращает словарь users
@app.get("/users")
async def get_users():
    return users

#Пример: Создать нового юзера
@app.post("/user/{username}/{age}")
async def create_new_user(
    username: Annotated[str, Path(min_length=5, max_length=20,
                                    description="Enter username", example="Username29")],
    age: Annotated[int, Path(ge=18, le=120,
                                  description="Enter age", example="24")]
):
    current_index = str(int(max(users, key=int))+1)
    users[current_index] = f"Имя: {username}, возраст: {age}"
    return f"User {username} is registered!"


# Update (PUT): Обновление данных

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
    user_id: Annotated[int, Path(description="Enter User ID")],
    username: Annotated[str, Path(min_length=5, max_length=20,
                                    description="Enter username", example="Username29")],
    age: Annotated[int, Path(ge=18, le=120,
                                  description="Enter age", example="24")]
):
    if str(user_id) in users:
        users[user_id] = f"Имя: {username}, возраст: {age}"
        return f'The user {user_id} is updated'
    else:
        raise HTTPException(status_code=404, detail="Юзер не найден")

#raise HTTPException(status_code=404, detail="Задача не найдена")

# Delete (DELETE): Удаление юзера

@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    if str(user_id) in users:
        users.pop(str(user_id))
        return f"User {user_id} was deleted!"
    else:
        raise HTTPException(status_code=404, detail="Юзер не найден")
