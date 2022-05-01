from tempfile import NamedTemporaryFile
from datetime import datetime, timezone
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pylinac import WinstonLutz


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return


@app.post("/pdf/")
async def pdf(file: UploadFile):

    try:
        contents = await file.read()
        file_copy = NamedTemporaryFile(delete=False)
        with file_copy as f:
            f.write(contents)
        wl = WinstonLutz.from_zip(file_copy.name)
        wl.analyze()
        filename = "WL_result_{}.pdf".format(
            datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        )
        wl.publish_pdf(filename)

        return FileResponse(filename, media_type="application/pdf")

    except Exception as e:
        return {"exception": print(e)}


@app.post("/results/")
async def results(file: UploadFile):

    try:
        contents = await file.read()
        file_copy = NamedTemporaryFile(delete=False)
        with file_copy as f:
            f.write(contents)
        wl = WinstonLutz.from_zip(file_copy.name)
        wl.analyze()
        data_dict = wl.results_data(as_dict=True)
        return data_dict

    except Exception as e:
        return {"exception": print(e)}


@app.get("/testapi/")
async def testapi():

    return {"message": "It works!"}
