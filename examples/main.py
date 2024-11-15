from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from KDOne.api import KDOneAPI
from KDOne.models.device import DeviceType
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

kd_one = KDOneAPI(username="", password="")


class LoginRequest(BaseModel):
    username: str
    password: str
    complex_id: str


class CertifyRequest(BaseModel):
    certify_number: str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/login")
async def login(request: LoginRequest):
    global kd_one
    kd_one = KDOneAPI(username=request.username, password=request.password)
    kd_one.login(request.complex_id)
    return JSONResponse(
        {"message": "Login successful. Please enter the certification code."}
    )


@app.post("/certify")
async def certify(request: CertifyRequest):
    kd_one.certify(request.certify_number)
    kd_one.get_token()
    return JSONResponse({"message": "Certification successful."})


@app.get("/devices")
async def get_devices():
    devices = kd_one.get_devices(DeviceType.LIGHT)
    return JSONResponse({"message": f"Devices: {devices}"})


@app.get("/call-elevator")
async def call_elevator():
    kd_one.call_elevator()
    return JSONResponse({"message": "Elevator called."})
