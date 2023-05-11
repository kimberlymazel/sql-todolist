from sqlalchemy.orm import Session
from sqlalchemy import delete
from . import models, schemas

# ------------------------------------------------------------#
# ------------------------------------------------------------#
# ---------------------- USER METHODS ------------------------#
# ------------------------------------------------------------#
# ------------------------------------------------------------#

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_userlist(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.CreateUser):
    db_user = models.User(username=user.username, email=user.email, auth=user.auth)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ------------------------------------------------------------#
# ------------------------------------------------------------#
# ---------------------- TASK METHODS ------------------------#
# ------------------------------------------------------------#
# ------------------------------------------------------------#

def create_user_task(db: Session, task: schemas.CreateTask, user_id: int):
    db_task = models.Task(**task.dict(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasklist(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()