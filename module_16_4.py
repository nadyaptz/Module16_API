from fastapi import FastAPI, Path
from typing import Annotated, List
from pydantic import BaseModel, Field
from enum import Enum
from fastapi import HTTPException

# uvicorn module_16_4:app --reload


# Создаем экземпляр приложения FastAPI

app = FastAPI()


class User(BaseModel):
    id: int = None
    username: str
    age: int


users = []


# возвращает cписок users
@app.get("/users", response_model=List[User])
async def get_users():
    return users


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
