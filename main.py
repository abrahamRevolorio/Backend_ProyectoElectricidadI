from fastapi import FastAPI, Request,  HTTPException, WebSocket, WebSocketDisconnect
import requests
from models.pico import Pico
from utils.pico_state import setPicoIp, getPicoIp
from utils.validators import validarIp
from utils.led_state import getLedState, setLedState
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

activeConnections = []

@app.websocket("/ws/{idDispositivo}")
async def websocket_endpoint(websocket: WebSocket, deviceId: str):
    
    await websocket.accept()

    activeConnections[idDispositivo] = websocket

    idDispositivo = websocket.cliente.host

    setPicoIp(f"http://{idDispositivo}")

    print(f"Raspberry Pi con IP {idDispositivo} conectado")

    try:

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:

        print(f"Raspberry Pi con IP {idDispositivo} desconectado")

        activeConnections.pop(idDispositivo, None)




@app.post("/configs/setPicoIp")
async def setPico_Ip(request: Request):

    try:

        body = await request.json()

        idLocal = body.get("ip")

        if not idLocal:

            raise HTTPException(status_code=400, detail="Ip no proporcionada")
        
        ipFormateada = validarIp(idLocal)

        setPicoIp(ipFormateada)

    except Exception as e:

        raise HTTPException(status_code=400, detail="Ip Invalida")

@app.post("/led/on")
async def ledOn():

    idsDipositivo = "raspi-001"

    websocket = activeConnections.get(idsDipositivo)

    if websocket:

        try:

            await websocket.send_json({"command": "led_on"})

            setLedState(True)

            return {"status": "Led encendido via websocket"}
        
        except Exception as e:

            raise HTTPException(status_code=400, detail="Error al encender led")

    ip = getPicoIp()

    if not ip:
        return {"status": "Error!", "error": "Raspberry no conectada"}
    
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
async def ledOff():

    idsDipositivo = "raspi-001"

    websocket = activeConnections.get(idsDipositivo)

    if websocket:

        try:

            await websocket.send_json({"command": "led_off"})

            setLedState(False)

            return {"status": "Led apagado via websocket"}
        
        except Exception as e:

            raise HTTPException(status_code=400, detail="Error al apagar led")

    ip = getPicoIp()

    if not ip:
        return {"status": "Error!", "error": "Raspberry no conectada"}
    
    try:

        r = requests.get(f"{ip}/led/off")
        setLedState(False)
        return {"status": "Done", "led": "off", "pico_response": r.json()}
    
    except Exception as e:

        if "Max retries exceeded" in str(e) or "ConnectionTimeoutError" in str(e):

            return {"status": "Error!", "error": "Pico no disponible"}
        
        else:

            return {"status": "Error!", "error": str(e)}

