from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, database
from blog.crud.blog import get_all, create, get_one, update_one, destroy_one
from ..oauth2 import get_current_user

router = APIRouter(
    tags=['blogs']
)

# create a blog
@router.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return create(request, db)

# get all blogs
@router.get("/blogs", response_model=List[schemas.ShowBlog])
def get_blogs(db: Session=Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return get_all(db)


# get a blog
@router.get("/blog/{id}", response_model=schemas.ShowBlog)
def get_blog(id, response: Response, db: Session=Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return get_one(id, response, db)

# update a blog
@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.Blog, db: Session=Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return update_one(id, request, db)


# delete a blog
@router.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session=Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return destroy_one(id, db)


