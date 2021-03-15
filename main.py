from typing import Optional, List
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse

import base64
import io

import locale
locale.setlocale(locale.LC_ALL, 'C')
from PIL import Image
Image.MAX_IMAGE_PIXELS=1000000000
from tesserocr import PyTessBaseAPI, RIL, iterate_level, PSM, OEM


folder = 'static/'
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

class ImageModel(BaseModel):
    base64: str
class ImageItemResp(BaseModel):
    text: str
    width: int
    height: int
    left: int
    top: int
class ImageModalResp(BaseModel):
    texts: List[ImageItemResp]


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
    
@app.get("/about/")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.post('/upload/')
def upload(request: ImageModel): 
    msg = base64.b64decode(request.base64)
    buf = io.BytesIO(msg)
    image = Image.open(buf)


    with PyTessBaseAPI(oem=OEM.LSTM_ONLY) as api:
        api.SetImage(image)
        api.Recognize()
        api.SetVariable("save_blob_choices","T")
        ri=api.GetIterator()
        level=RIL.TEXTLINE
        boxes = api.GetComponentImages(RIL.TEXTLINE, True)
        text_list = []
        i = 0
        for r in iterate_level(ri, level):
            symbol = r.GetUTF8Text(level)
            conf = r.Confidence(level)
            bbox = r.BoundingBoxInternal(level)
            im = {
                "text": symbol,
                "left": bbox[0],
                "top": bbox[1],
                "width": bbox[2] - bbox[0],
                "height": bbox[3] - bbox[1],
            }
            text_list.append(im)
            i += 1
    return {
        "texts": text_list,
    }
