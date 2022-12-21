import sys
from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from db import SessionLocal, Base, engine
import models


try:
    Base.metadata.create_all(engine)  # Creating the database if not already exists.
except:
    print("Failed accessing the database")
    sys.exit(-1)


app = FastAPI()


class User(BaseModel):  # Serializer
    id: Optional[int]  # Optional so it's unnecessary in a post req (handled automatically by DB), but still gets displayed in a get req.
    name: str
    email: str

    class Config:
        orm_mode = True


def get_db():  # For dependency injection
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API Endpoints
@app.get("/", status_code=status.HTTP_200_OK)
async def root():  # Home
    return {"message": "Welcome to my user-management API :)"}


# Get all users data
@app.get("/users", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


# Get a specific user's data
@app.get("/user/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==user_id).first()
    return user


# Add a user to the database.
@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User, db: Session = Depends(get_db)):
    # Checking if the user already exists in the database.
    db_user = db.query(models.User).filter(models.User.name==user.name).first()
    if db_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = models.User(name=user.name, email=user.email)

    db.add(new_user)
    db.commit()
    return new_user


# Update a user's data.
@app.put("/user/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    user_to_update = db.query(models.User).filter(models.User.id==user_id).first()

    user_to_update.name = user.name
    user_to_update.email = user.email

    db.commit()
    return user_to_update


# Delete a user from the database
@app.delete("/user/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_to_delete = db.query(models.User).filter(models.User.id==user_id).first()

    if user_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(user_to_delete)
    db.commit()
    return user_to_delete
