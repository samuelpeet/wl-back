from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from pylinac import WinstonLutz

app = FastAPI()


@app.get("/")
async def root():
    return


@app.post("/pdf/")
async def pdf(file: UploadFile):

    wl = WinstonLutz.from_zip(file.filename)
    wl.analyze()
    # data_dict = wl.results_data(as_dict=True)
    wl.publish_pdf("temp/mywl.pdf")

    return FileResponse("temp/mywl.pdf")


@app.post("/results/")
async def results(file: UploadFile):

    wl = WinstonLutz.from_zip("winston_lutz.zip")
    wl.analyze()
    data_dict = wl.results_data(as_dict=True)

    return data_dict
