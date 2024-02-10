from typing import Annotated
from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

app = FastAPI()


class IngredientBase(BaseModel):
    name: str


class UserBase(BaseModel):
    username: str
    password: str


class RecipeBase(BaseModel):
    title: str
    description: str
    prep_time: str
    cook_time: str
    total_time: str
    level: str
    rating: int
    people: int

    ingredients: list[IngredientBase]


# class RecipeIngredients(BaseModel):
#     ingredients_id: str
#     ingredient: list[IngredientBase]


def get_recipes_db():
    recipes_db = SessionLocal()
    try:
        yield recipes_db
    finally:
        recipes_db.close()


db_dependency = Annotated[Session, Depends(get_recipes_db)]
# jawbone = session.query(Company).filter_by(name="Jawbone").first()


# Corrected db_dependency usage
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Updated get_or_create function signature
def get_or_create(session: Session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance, True

# Correctly use the dependency
@app.post("/recipes/", status_code=status.HTTP_201_CREATED)
async def create_recipe(recipe: RecipeBase, db: Session = Depends(get_db)):
    ingredient_models = []
    for ingredient in recipe.ingredients:
        ing_model, created = get_or_create(db, models.Ingredients, name=ingredient.name)
        ingredient_models.append(ing_model)

    # Assume models.Recipe is an SQLAlchemy model with a correct relationship setup
    recipe_model = models.Recipe(
        title=recipe.title,
        description=recipe.description,
        prep_time=recipe.prep_time,
        cook_time=recipe.cook_time,
        total_time=recipe.total_time,
        level=recipe.level,
        rating=recipe.rating,
        people=recipe.people,
        ingredients=ingredient_models  # This assumes a relationship is set up in the models
    )
    db.add(recipe_model)
    db.commit()
    db.refresh(recipe_model)

@app.get("/recipes/{recipes_name}", status_code=status.HTTP_200_OK)
async def read_recipe(recipe_name: str, db: db_dependency):
    recipe = db.query(models.Recipe).filter(models.Recipe.title == recipe_name).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="User non found")

    return recipe


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User non found")
    return user


models.Base.metadata.create_all(bind=engine)
