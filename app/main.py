from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine
from app.users.router.auth import router as auth_router
from app.courses.router.courses import router as courses_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(courses_router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@app.get("/")
def root():
    return {"message": "Welcome to Gabcursos"}
