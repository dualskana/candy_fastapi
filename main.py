from fastapi import FastAPI

from api import users, auth, items, letters
from db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(auth.router,  tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(items.router, prefix="/items", tags=["Items"])
app.include_router(letters.router, prefix="/letter", tags=["Letter"])
