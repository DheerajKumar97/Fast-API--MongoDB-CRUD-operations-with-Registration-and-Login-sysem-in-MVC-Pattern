import uvicorn
import logging
from fastapi import FastAPI, Request, Body, Depends, Header
from starlette.responses import JSONResponse
from register.route import register_rt
from login.route import login_rt
from operations.route import operation_rt
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(register_rt)
app.include_router(login_rt)
app.include_router(operation_rt)
logging.basicConfig(filename='app_logs.log', level=logging.DEBUG)


@app.get("/page")
async def get_headers():
    content = {"message": "Hello World"}
    headers = {"Content-Type": "application/json", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)