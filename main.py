from fastapi import FastAPI
from api.auth.views import router as auth_router

app = FastAPI()
app.include_router(auth_router)

@app.get("/")
def main_page():
    return "Hello, user"