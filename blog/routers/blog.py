from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, database


router = APIRouter(

)

# create a blog
@router.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blogs"])
def blog(request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_post =  models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# get all blogs
@router.get("/blogs", response_model=List[schemas.ShowBlog], tags=["blogs"])
def get_blogs(db: Session=Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return  blogs

# get a blog
@router.get("/blog/{id}", response_model=schemas.ShowBlog, tags=["blogs"])
def get_blog(id, response: Response, db: Session=Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} is not found!")
    return blog

# update a blog
@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def update_blog(id, request: schemas.Blog, db: Session=Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} is not found!")
    blog.update(request)
    db.commit()
    return f"Post with id {id} Updated!"


# delete a blog
@router.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def delete_blog(id, db: Session=Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} is not found!")
    blog.delete()
    db.commit()
    return "Post with id {id} deleted!"


