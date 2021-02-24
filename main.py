from fastapi import FastAPI
import uvicorn

# module import
from  blog import models
from blog.database import engine

from blog.database import get_db
from blog.routers import blog, user


app = FastAPI(title="Postmani!") #

# routes registry
app.include_router(blog.router)
app.include_router(user.router)

models.Base.metadata.create_all(bind=engine)





# users routes



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)