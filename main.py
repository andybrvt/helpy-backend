from fastapi import FastAPI
from routers import user, alexa, task, community,care_staff,room  # Import the user router
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
app.include_router(alexa.router, prefix="/api", tags=["alexa"])
app.include_router(task.router, prefix="/api", tags=["tasks"])
app.include_router(community.router, prefix="/api", tags=["communities"])  
app.include_router(care_staff.router, prefix="/api", tags=["care_staff"])  
app.include_router(room.router, prefix="/api", tags=["rooms"])  # Added room router


