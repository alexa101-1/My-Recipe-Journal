from typing import Annotated

from fastapi import FastAPI, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class UserBase(BaseModel):
    username: str
    password: str


class RecipeBase(BaseModel):
    title: str
    description: str
    # ingredients: [str]
    prep_time: str
    cook_time: str
    total_time: str
    level: str
    rating: int
    people: int


def get_recipes_db():
    recipes_db = SessionLocal()
    try:
        yield recipes_db
    finally:
        recipes_db.close()


db_dependency = Annotated[Session, Depends(get_recipes_db)]


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
