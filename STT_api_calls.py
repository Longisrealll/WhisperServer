from typing import Union
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from STT_handler import STT_handler
import asyncio
from contextlib import asynccontextmanager
import os
from datetime import datetime
import shutil

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Configuating.......")
    app.state.callingHandle = STT_handler("turbo")
    yield
    if os.path.exists(f".\\preDatabase"):
        shutil.rmtree(f".\\preDatabase")
    print("Shutting down")

app = FastAPI(lifespan=lifespan)

@app.post("/uploadFile")
async def acceptWebm(file: UploadFile = File(...)):
    DATABASEDIR = ".\\preDatabase\\"
    filenamePreprocess = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    filePath = os.path.join(DATABASEDIR, f"{filenamePreprocess}.webm")
    with open(filePath, "wb") as files:
        files.write(await file.read())

    res = app.state.callingHandle.set_data(filePath)

    return {"status":"ok", "result": {"text": res['text'], "language": res["language"]}}

app.mount("/", StaticFiles(directory="static", html=True), name="static")
