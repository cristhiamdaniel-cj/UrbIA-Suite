from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from typing import Any

app = FastAPI()
monitor: Any = None  # Se inyectará desde SDNMonitor

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/stats/flows")
def get_flow_stats():
    if monitor is None:
        return JSONResponse(status_code=503, content={"error": "Monitor SDN no inicializado"})
    return monitor.stats_switches

@app.get("/stats/ports")
def get_port_stats():
    if monitor is None:
        return JSONResponse(status_code=503, content={"error": "Monitor SDN no inicializado"})
    return monitor.stats_puertos

def lanzar_api(monitor_sdn):
    global monitor
    monitor = monitor_sdn
    uvicorn.run(app, host="0.0.0.0", port=8028)
