import os

from cargo_service import cargo_service,cargo_alchemy_service
from fastapi import  FastAPI
import uvicorn
from dotenv import load_dotenv

load_dotenv()



app=FastAPI()


app.include_router(cargo_service.router,tags=["CARGO"])
app.include_router(cargo_alchemy_service.router,tags=["Cargo_pagination_sqlalchemy"])



@app.get("/")
def read_root():
    return {"message":"welcome user, Explorer the task"}


if __name__=="__main__":
    # uvicorn.run("main:app",host=os.getenv("DB_HOST"),port=int(os.getenv("DB_PORT")))
    uvicorn.run("main:app", host="localhost", port=59904)