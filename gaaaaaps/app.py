import json
import traceback
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from utils import error_response, ok_response, \
                  ok_response_table, get_data, \
                  get_info, get_station, get_list_for_form
from config import get_www_config

app = FastAPI(debug=True)

# Montez le répertoire contenant vos fichiers statiques (par exemple, 'static')
app.mount("/static", StaticFiles(directory="static"), name="static")

# Définissez une route pour servir votre page HTML
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    with open("/app/gaaaaaps/app.html", "r") as file:
        content = file.read()
    return content

@app.get("/test")
async def root():
    return {"message": "Hello World"}

@app.post('/ws/get_data')
async def get_table(request: Request):
    try:
        s_form = await request.body()
        form = json.loads(s_form)
        data, keys = get_data(form)
        return ok_response_table(data=data, keys=keys)
    except Exception:
        return error_response('%s' % traceback.format_exc())


@app.post('/ws/day')
async def get_info_station(request: Request):
    try:
        s_detail = await request.body()
        detail = json.loads(s_detail)
        info = get_info(detail)
        return ok_response(info)
    except Exception:
        return error_response('%s' % traceback.format_exc())


@app.post('/ws/station')
async def get_statistics_station(request: Request):
    try:
        s_detail = await request.body()
        detail = json.loads(s_detail)
        info = get_station(detail)
        return ok_response(info)
    except Exception:
        return error_response('%s' % traceback.format_exc())


@app.post('/ws/year')
async def get_year():
    try:
        return ok_response(get_www_config()["available_year"])
    except Exception:
        return error_response('%s' % traceback.format_exc())


@app.post('/ws/form')
async def get_form(request: Request):
    try:
        s_detail = await request.body()
        detail = json.loads(s_detail)
        print(detail)
        projet = get_list_for_form(detail['val'])
        print(projet)
        return ok_response(projet)
    except Exception:
        return error_response('%s' % traceback.format_exc())

#{
#  "rangedate": "",
#  "s_date": 1,
#  "e_date": 2,
#  "y_date": "2020-12-31T23:00:00.000Z",
#  "comp": [],
#  "type": [],
#  "loc": [],
#  "sta": [],
#  "more_option": false,
#  "network": [],
#  "julian_day": true,
#  "visible": false
#}

@app.get('/ws/comment')
async def set_comment(sds: str, year: str, net: str, sta: str, day: str):
    if not all([sds, year, net, sta, day]):
        raise HTTPException(status_code=400, detail="Missing parameters")
