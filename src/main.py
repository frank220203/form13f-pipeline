import uvicorn
from fastapi import FastAPI
from adapter.gateways.router import Router

app = FastAPI()
router = Router()
app.include_router(router.get_router())

@app.get("/")
def main():
    return {"message": "Form 13F Pipeline Service is working"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)