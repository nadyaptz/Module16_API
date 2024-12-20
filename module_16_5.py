from fastapi import FastAPI, Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates
from typing import Annotated, List

# uvicorn module_16_5:app --reload


# Создаем экземпляр приложения FastAPI

app = FastAPI()
# Настраиваем Jinja2 для загрузки шаблонов из папки templates
templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id: int = None
    username: str
    age: int


# users = []
users: List[User] = [
    User(id=1, username="User1", age=18),
    User(id=2, username="User2", age=28)
]


# Основная страница (GET-запрос)

@app.get("/", response_class=HTMLResponse)
async def get_main_page(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

# Детали юзеров (GET-запрос)

@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_users(request: Request, user_id: Annotated[int, Path(ge=1)]):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User not found")

#Пример: Создать нового юзера

class CreateUser(BaseModel):
    username: str = Field(..., min_length=5, max_length=20,
                          description="Enter Username")
    age: int = Field(..., ge=18, le=120, description="Enter age")


@app.post("/user", response_model=User)
async def create_new_user(user: CreateUser):
    current_index = max((u.id for u in users), default=0) + 1
    new_user = User(id=current_index, username=str(user.username), age=user.age)
    users.append(new_user)
    return new_user


# Update (PUT): Обновление данных

@app.put("/user/{user_id}", response_model=User)
async def update_user(user_id: int, user: CreateUser):
    for u in users:
        if u.id == user_id:
            u.username = user.username
            u.age = user.age
            return u
    raise HTTPException(status_code=404, detail="Юзер не найден")


# Delete (DELETE): Удаление юзера

@app.delete("/user/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    for i, u in enumerate(users):
        if u.id == user_id:
            del users[i]
            return {"detail": f"Юзер {user_id} удален"}
    raise HTTPException(status_code=404, detail="Юзер не найден")
