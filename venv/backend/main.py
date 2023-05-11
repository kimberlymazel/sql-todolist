from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def index():
    return {"FastAPI": "SQL Database"}

# ------------------------------------------------------------#
# ------------------------------------------------------------#
# ---------------------- USER METHODS ------------------------#
# ------------------------------------------------------------#
# ------------------------------------------------------------#

# CREATE A NEW USER
@app.post("/create-user/", response_model=schemas.User)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# GET ALL USERS
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_userlist(db, skip=skip, limit=limit)
    return users

# GET USER BY ID
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# DELETE USER BY ID
@app.delete("/delete-user/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db, user_id=user_id)

# ------------------------------------------------------------#
# ------------------------------------------------------------#
# ---------------------- TASK METHODS ------------------------#
# ------------------------------------------------------------#
# ------------------------------------------------------------#

# CREATE A TASK
@app.post("/users/{user_id}/tasklist/", response_model=schemas.Task)
def create_task_for_user(
    user_id: int, task: schemas.CreateTask, db: Session = Depends(get_db)):
    return crud.create_user_task(db=db, task=task, user_id=user_id)

# GET ALL TASKS
@app.get("/tasklist/", response_model=list[schemas.Task])
def read_task(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasklist(db, skip=skip, limit=limit)
    return tasks