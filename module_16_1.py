from fastapi import FastAPI
from pydantic import BaseModel

# запуск сервера:
# uvicorn module_16_1:app --reload
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
async def user_page(user_id: str):
    '''
    Get User ID
    '''
    return {f"Вы вошли как пользователь {user_id}"}

@app.get("/user")
async def id_user_page(username: str, age: int) -> dict:
    '''
    Get User Info
    '''
    return {"": f"Информация о пользователе. Имя: {username}, Возраст: {age}"}