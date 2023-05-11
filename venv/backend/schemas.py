from pydantic import BaseModel

class TaskBase(BaseModel):
    name: str
    description: str
    completed: bool

class CreateTask(TaskBase):
    pass

class Task(TaskBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
    
class UserBase(BaseModel):
    username: str
    email: str
    auth: str

class CreateUser(UserBase):
    pass

class User(UserBase):
    id: int
    tasklist: list[Task] = []

    class Config:
        orm_mode = True