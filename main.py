from fastapi import FastAPI
from routers import user  # Import the user router
from fastapi.middleware.cors import CORSMiddleware


# post, put, delete
# authentication
# database setup


app = FastAPI()

origins = [
    "http://localhost:3000",  # React app URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# Include the user router
app.include_router(user.router, prefix="/api", tags=["users"])
