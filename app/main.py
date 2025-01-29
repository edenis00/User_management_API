from fastapi import FastAPI
from app.routes import user_routes
from app.database import Base, engine

app = FastAPI()

app.include_router(user_routes.router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Welcome user!"}
