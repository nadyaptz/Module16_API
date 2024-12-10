from fastapi import FastAPI, Path
from typing import Annotated
from pydantic import BaseModel
from enum import Enum

# запуск сервера:
# uvicorn module_16_2:app --reload


# Создаем экземпляр приложения FastAPI

app = FastAPI()

# Определение базового маршрута
@app.get("/")
async def get_main_page():
    '''
    Get Main Page
    '''
    return {"Главная страница"}

@app.get("/user/admin")
async def user_admin():
    '''
    Get Admin Page
    '''
    return {"Вы вошли как администратор"}

@app.get("/user/{user_id}")
async def user_page(user_id: Annotated[int, Path(ge=1, le=100, title="User ID",
                                                 description="Enter User ID", example='15')]):
    '''
    Get User ID
    '''
    return {f"Вы вошли как пользователь {user_id}"}

@app.get("/user/{username}/{age}")
async def id_user_page(
    username: Annotated[str, Path(min_length=5, max_length=20,
                                    description="Enter username", example="Username29")],
    age: Annotated[int, Path(ge=18, le=120,
                                  description="Enter age", example="24")]
):
    '''
    Get User Info
    '''
    return {"message": f"Информация о пользователе. Имя: {username}, Возраст: {age}"}