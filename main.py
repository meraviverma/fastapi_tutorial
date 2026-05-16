from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@app.get("/about")
def about():
    return {"message": "This is a simple FastAPI application with about"}

@app.get("/contact")
def contact():
    return {"message": "Contact us at example@email.com"}