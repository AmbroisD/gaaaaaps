import json
import traceback
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import JSONResponse, HTMLResponse
from starlette.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from utils import error_response, ok_response, \
                  ok_response_table, get_data, \
                  get_info, get_station, get_list_for_form, \
                  generate_csv_response, get_avg
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
        projet = get_list_for_form(detail['val'])
        return ok_response(projet)
    except Exception:
        return error_response('%s' % traceback.format_exc())
    

@app.get('/ws/comment')
async def set_comment(sds: str, year: str, net: str, sta: str, day: str):
    if not all([sds, year, net, sta, day]):
        raise HTTPException(status_code=400, detail="Missing parameters")
    

@app.get("/ws/get_avg/")
async def get_avg_api(year: str = Query(..., description="Year in string format ('YYYY')"),
                      j_starttime: int = Query(..., description="Start time as Julian day"),
                      j_endtime: int = Query(..., description="End time as Julian day"),
                      format: str = Query('json', description="Output format: json or csv")):
    """
    API endpoint to calculate the average percentage for each channel between two given time periods.

    Args:
        year (str): Year in string format ('YYYY').
        j_starttime (int): Start time as Julian day.
        j_endtime (int): End time as Julian day.
        format (str): Output format, either 'json' or 'csv'.

    Returns:
        JSON or CSV response based on the requested format.
    """
    try:
        data, keys = get_avg(year, j_starttime, j_endtime)
        
        if format == 'csv':
            csv_data = generate_csv_response(data)
            return StreamingResponse(iter([csv_data]), media_type="text/csv",
                                     headers={"Content-Disposition": f"attachment; filename=average_gap.csv"})
            #response = generate_csv_response(data)
            #return response
        else:
            return ok_response_table(data=data)
    except Exception:
        return error_response('%s' % traceback.format_exc())