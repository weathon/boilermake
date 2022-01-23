from typing import List
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
app = FastAPI()
import io
import base64
from io import BytesIO
import random
import numpy as np
# import tensorflow_hub as hub
# import tensorflow as tf


# import tensorflow_hub as hub
# hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

@app.get("/", response_class=HTMLResponse)
async def read_items():
    f = open("BM/index.html","r")
    t = f.read()
    f.close()
    return t

def load_img(path_to_img):
  max_dim = 512
  img = tf.io.read_file(path_to_img)
  img = tf.image.decode_image(img, channels=3)
  img = tf.image.convert_image_dtype(img, tf.float32)

  shape = tf.cast(tf.shape(img)[:-1], tf.float32)
  long_dim = max(shape)
  scale = max_dim / long_dim

  new_shape = tf.cast(shape * scale, tf.int32)

  img = tf.image.resize(img, new_shape)
  img = img[tf.newaxis, :]
  return img



@app.post("/action/", response_class=HTMLResponse)
async def create_file(file: bytes  = File(...)):
    # file.write(file.filename)
    img = Image.open(io.BytesIO(file)).resize((255,255))
    buffered = BytesIO()
    img.save(buffered, format="png")
    img_str = base64.b64encode(buffered.getvalue())
    with open("BM/after.html","r") as f:
        t=f.read()
    t=t.replace("{{ss}}","data:image/png;base64,"+img_str.decode())
    bg = Image.open("croped/%s.png" % random.randint(0,475))
    new_img = Image.fromarray((np.array(bg).astype("float16")/2+np.array(img).astype("float16")/2).astype("uint8"))
    buffered = BytesIO()
    new_img.save(buffered, format="png")
    img_str = base64.b64encode(buffered.getvalue())
    t=t.replace("{{tm}}","data:image/png;base64,"+img_str.decode())

    # buffered = BytesIO()
    # img.save(buffered, format="png")
    # content_image = load_img(buffered)
    # style_image = load_img("croped/%s.png" % random.randint(0,475))



    return t

# from typing import List

# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import HTMLResponse

# app = FastAPI()


# @app.post("/files/")
# async def create_files(files: List[bytes] = File(...)):
#     return {"file_sizes": [len(file) for file in files]}


# @app.post("/uploadfiles/")
# async def create_upload_files(files: List[UploadFile] = File(...)):
#     return {"filenames": [file.filename for file in files]}


# @app.get("/")
# async def main():
#     content = """
# <body>
# <form action="/files/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)