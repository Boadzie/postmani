from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, database
from blog.hashing import Hash

router = APIRouter()


# create a user
@router.post("/user", response_model=schemas.ShowUser, tags=["users"])
def create_user(request: schemas.User, db: Session=Depends(database.get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# get all users
@router.get("/users", response_model=List[schemas.ShowUser], tags=["users"])
def get_all_users(db: Session=Depends(database.get_db)): 
    users = db.query(models.User).all()
    return users

# get a user
@router.get("/user/{id}", response_model=schemas.ShowUser, tags=["users"])
def get_user(id: int, db: Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} is not found!")
    return user 

# update a user
@router.put("/user/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["users"])
def update_user(id, request: schemas.User, db: Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not found!")
    user.update(request)
    db.commit()
    return f"User with id {id} Updated!"


# delete a blog
@router.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: int, db: Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not found!")
    user.delete()
    db.commit()
    return "User with id {id} deleted!"
