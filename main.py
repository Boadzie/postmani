from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
import uvicorn
from typing import List
# module import
from  blog import schemas, models
from blog.database import engine, SessionLocal

app = FastAPI(title="Postmani!") #

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create a blog
@app.post("/blog", status_code=status.HTTP_201_CREATED)
def blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_post =  models.Blog(title=request.title, body=request.body)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# get all blogs
@app.get("/blogs", response_model=List[schemas.ShowBlog])
def get_blogs(db: Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return  blogs

# get a blog
@app.get("/blog/{id}", response_model=schemas.ShowBlog)
def get_blog(id, response: Response, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} is not found!")
    return blog

# update a blog
@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.Blog, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} is not found!")
    blog.update(request)
    db.commit()
    return f"Post with id {id} Updated!"


# delete a blog
@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} is not found!")
    blog.delete()
    db.commit()
    return "Post with id {id} deleted!"



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)