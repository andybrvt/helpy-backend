from fastapi import FastAPI
from routers import user  # Import the user router

# post, put, delete
# authentication
# database setup


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# Include the user router
app.include_router(user.router, prefix="/api", tags=["users"])
