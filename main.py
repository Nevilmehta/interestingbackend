from fastapi import FastAPI
from api.routes import users, auth, admin
from core.middleware import RateLimitMiddleware
from core.tasks import email

app = FastAPI(title="Backend Mastery")

app.add_middleware(RateLimitMiddleware)

@app.get("/")
def read_root():
    return {"message": "Welcome to Backend Mastery App"}

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])