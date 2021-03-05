from typing import Optional, List
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

import base64
import io

from PIL import Image
Image.MAX_IMAGE_PIXELS=1000000000
from tesserocr import PyTessBaseAPI, RIL, iterate_level



app = FastAPI()
templates = Jinja2Templates(directory="templates")

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
    return templates.TemplateResponse("main.html", {"request": request})

def transformCorInWidthInHeight(img):
    width = img.width - img.left
    height = img.height - img.top
    return {
        width: width,
        height: height,
    }



@app.post('/upload/')
def upload(request: ImageModel): 
    msg = base64.b64decode(request.base64)
    buf = io.BytesIO(msg)
    image = Image.open(buf)
    print('____buff', image);
    
    with PyTessBaseAPI() as api:
        api.SetImage(image)
        api.Recognize()
        api.SetVariable("save_blob_choices","T")
        ri=api.GetIterator()
        level=RIL.WORD
        boxes = api.GetComponentImages(RIL.TEXTLINE, True)
        text_list = []
        print('Found {} textline image components.'.format(len(boxes)))
        i = 0
        for r in iterate_level(ri, level):
            symbol = r.GetUTF8Text(level)
            conf = r.Confidence(level)
            bbox = r.BoundingBoxInternal(level)
            print(bbox, symbol, conf)
            im = {
                "text": symbol,
                "left": bbox[0],
                "top": bbox[1],
                "width": bbox[2],
                "height": bbox[3],
            }
            text_list.append(im)
            i += 1
        print('text_list', text_list)
    return {
        "texts": text_list,
    }