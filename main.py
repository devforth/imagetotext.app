from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from PIL import Image
Image.MAX_IMAGE_PIXELS=1000000000
from tesserocr import PyTessBaseAPI, RIL, iterate_level
import base64
import io

app = FastAPI()

class ImageModel(BaseModel):
    base64: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


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
        boxes = api.GetComponentImages(RIL.WORD, True)
        print('Found {} textline image components.'.format(len(boxes)))
        for r in iterate_level(ri, level):
            symbol = r.GetUTF8Text(level)
            conf = r.Confidence(level)
            print('_____asdsadasd___', r)
            if symbol:
                print(u'symbol {},conf: {}\n'.format(symbol,conf).encode('utf-8'))
    return {}