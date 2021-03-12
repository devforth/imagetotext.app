from typing import Optional, List
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import base64
import io
import os

import locale
locale.setlocale(locale.LC_ALL, 'C')
from PIL import Image
Image.MAX_IMAGE_PIXELS=1000000000
from tesserocr import PyTessBaseAPI, RIL, iterate_level, PSM, OEM
import cv2
import numpy as np


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

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

def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))

def toRGB(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

def preprocess_image(image):
    img_not_noise = cv2.fastNlMeansDenoising(image, None, 10)
    img_B_A_W = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return img_B_A_W



@app.post('/upload/')
def upload(request: ImageModel): 
    msg = base64.b64decode(request.base64)
    buf = io.BytesIO(msg)
    image = Image.open(buf)
    cv2Img = toRGB(stringToImage(request.base64))
    processed_img = preprocess_image(cv2Img)

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, processed_img)
    
    

    # with PyTessBaseAPI(oem=OEM.LSTM_ONLY) as api:
    #     api.SetImage(image)
    #     api.Recognize()
    #     api.SetVariable("save_blob_choices","T")
    #     ri=api.GetIterator()
    #     level=RIL.TEXTLINE
    #     boxes = api.GetComponentImages(RIL.TEXTLINE, True)
    #     text_list = []
    #     i = 0
    #     for r in iterate_level(ri, level):
    #         symbol = r.GetUTF8Text(level)
    #         conf = r.Confidence(level)
    #         bbox = r.BoundingBoxInternal(level)
    #         im = {
    #             "text": symbol,
    #             "left": bbox[0],
    #             "top": bbox[1],
    #             "width": bbox[2] - bbox[0],
    #             "height": bbox[3] - bbox[1],
    #         }
    #         text_list.append(im)
    #         i += 1
    return {
        "texts": [],
    }
