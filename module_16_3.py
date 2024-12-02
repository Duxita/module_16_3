from fastapi import FastAPI, Path, HTTPException
from typing import Annotated

app = FastAPI()
# Словарь
users = {'1': 'Имя: Example, возраст: 18'}
@app.get("/user/{user_id}")
def get_user(user_id: int = Path(..., ge=1, le=100, description="Enter User ID")):
    return f"Вы вошли как пользователь № {user_id}"
@app.get("/user/{username}/{age}")
def get_user_info(
        username: Annotated[str, Path(min_length=5,
                                      max_length=20,
                                      pattern="^[A-Za-z0-9_-]+$",
                                      description="Enter username")],
        age: Annotated[int, Path(ge=18, le=120, description="Enter age")]
):
    return f"Информация о пользователе. Имя: {username}, Возраст: {age}"
@app.get("/users")
def get_users():
    return users
@app.get("/users/{user_id}")
async def get_all_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="Пользователь не найден")
@app.post("/user/{username}/{age}")
def create_user(username: str, age: int):
    user_id = str(max(map(int, users.keys()), default=0) + 1)
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"User {user_id} is registered"
@app.put("/user/{user_id}/{username}/{age}")
def update_user(user_id: str, username: str, age: int):
    if user_id in users:
        users[user_id] = f"Имя: {username}  возраст: {age}"
        return f"The user {user_id} is updated"
    else:
        raise HTTPException(status_code=404, detail=f"Пользователь {user_id} не найден")
@app.delete("/user/{user_id}")
def delete_user(user_id: str):
    if user_id in users:
        users.pop(user_id)
        return {"detail": f"User ID :{user_id} deleted!"}
    else:
        raise HTTPException(status_code=404, detail="User not found")