from typing import List
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
app = FastAPI()
import io
import base64
from io import BytesIO


@app.get("/", response_class=HTMLResponse)
async def read_items():
    f = open("BM/index.html","r")
    t = f.read()
    f.close()
    return t

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