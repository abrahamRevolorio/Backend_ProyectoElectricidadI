from fastapi import FastAPI,  HTTPException
import requests
from models.pico import Pico
from utils.pico_state import setPicoIp, getPicoIp
from utils.validators import validarIp
from utils.led_state import getLedState, setLedState

app = FastAPI()

@app.post("/configs/setPicoIp")
async def setPico_Ip(pico: Pico):

    try:

        ipFormateada = validarIp(pico.ip)

        setPicoIp(ipFormateada)

        return {"status": "Ip Configurada", "ip": getPicoIp()}

    except Exception as e:

        raise HTTPException(status_code=400, detail="Cuerpo de solicitud inválido o vacío")

@app.post("/led/on")
def ledOn():

    ip = getPicoIp()

    if not ip:
        return {"status": "Error!", "error": "Ip no configurada"}
    
    try:

        r = requests.get(f"{ip}/led/on")
        setLedState(True)
        return {"status": "Done", "led": "on", "pico_response": r.json()}
    
    except Exception as e:

        if "Max retries exceeded" in str(e) or "ConnectionTimeoutError" in str(e):

            return {"status": "Error!", "error": "Pico no disponible"}
        
        else:

            return {"status": "Error!", "error": str(e)}
        
@app.post("/led/off")
def ledOff():

    ip = getPicoIp()

    if not ip:
        return {"status": "Error!", "error": "Ip no configurada"}
    
    try:

        r = requests.get(f"{ip}/led/off")
        setLedState(False)
        return {"status": "Done", "led": "off", "pico_response": r.json()}
    
    except Exception as e:

        if "Max retries exceeded" in str(e) or "ConnectionTimeoutError" in str(e):

            return {"status": "Error!", "error": "Pico no disponible"}
        
        else:

            return {"status": "Error!", "error": str(e)}
    

