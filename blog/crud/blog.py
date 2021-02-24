from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from blog import models, database, schemas

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return  blogs

def create(request, db: Session):
    new_post =  models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_one(id, response, db: Session): 
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} is not found!")
    return blog

def update_one(id, request, db: Session): 
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} is not found!")
    blog.update(request)
    db.commit()
    return f"Post with id {id} Updated!"

def destroy_one(id, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} is not found!")
    blog.delete()
    db.commit()
    return "Post with id {id} deleted!"