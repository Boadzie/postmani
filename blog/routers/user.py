from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, database
from blog.hashing import Hash
from ..crud.user import create, get_one
from ..oauth2 import get_current_user

router = APIRouter(
 tags=["users"]
)


# create a user
@router.post("/user", response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session=Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return create(request, db)

# # get all users
# @router.get("/users", response_model=List[schemas.ShowUser])
# def get_all_users(db: Session=Depends(database.get_db)): 
#     users = db.query(models.User).all()
#     return users

# get a user
@router.get("/user/{id}", response_model=schemas.ShowUser)
def get_user(id: int, db: Session=Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return get_one(id, db)

# # update a user
# @router.put("/user/{id}", status_code=status.HTTP_202_ACCEPTED)
# def update_user(id, request: schemas.User, db: Session=Depends(database.get_db)):
#     user = db.query(models.User).filter(models.User.id == id)
#     if not user.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not found!")
#     user.update(request)
#     db.commit()
#     return f"User with id {id} Updated!"


# # delete a blog
# @router.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_user(id: int, db: Session=Depends(database.get_db)):
#     user = db.query(models.User).filter(models.User.id == id)
#     if not user.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not found!")
#     user.delete()
#     db.commit()
#     return "User with id {id} deleted!"
