from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect
import requests
from models.pico import Pico
from utils.pico_state import setPicoIp, getPicoIp
from utils.validators import validarIp
from utils.led_state import getLedState, setLedState
from fastapi.middleware.cors import CORSMiddleware

# Creamos el servidor
app = FastAPI()

# Permitimos conexiones desde cualquier lugar (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Guardamos conexiones activas por WebSocket
activeConnections = {}

# Ruta para conexión WebSocket
@app.websocket("/ws/{idDispositivo}")
async def websocket_endpoint(websocket: WebSocket, idDispositivo: str):
    await websocket.accept()  # Aceptamos la conexión

    # Guardamos conexión usando su ID
    activeConnections[idDispositivo] = websocket

    # Obtenemos la IP del cliente
    ipCliente = websocket.client.host
    setPicoIp(f"http://{ipCliente}")  # Guardamos IP

    print(f"Raspberry Pi con IP {ipCliente} conectado")

    try:
        while True:
            await websocket.receive_text()  # Escuchamos mensajes
    except WebSocketDisconnect:
        print(f"Raspberry Pi con IP {idDispositivo} desconectado")
        activeConnections.pop(idDispositivo, None)  # Quitamos conexión

# Ruta para guardar IP manualmente
@app.post("/configs/setPicoIp")
async def setPico_Ip(request: Request):
    try:
        body = await request.json()
        idLocal = body.get("ip")  # Leemos IP

        if not idLocal:
            raise HTTPException(status_code=400, detail="Ip no proporcionada")

        ipFormateada = validarIp(idLocal)  # Validamos IP
        setPicoIp(ipFormateada)  # Guardamos IP
    except Exception as e:
        raise HTTPException(status_code=400, detail="Ip Invalida")

# Ruta para encender LED
@app.post("/led/on")
async def ledOn():
    idDispositivo = "raspi-001"
    websocket = activeConnections.get(idDispositivo)

    if websocket:
        try:
            await websocket.send_json({"command": "led_on"})  # Enviamos orden
            setLedState(True)  # Actualizamos estado
            return {"status": "Led encendido via websocket"}
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error al encender led")

    ip = getPicoIp()  # Usamos IP si no hay WebSocket

    if not ip:
        return {"status": "Error!", "error": "Raspberry no conectada"}

    try:
        r = requests.get(f"{ip}/led/on")  # Encendemos por HTTP
        setLedState(True)
        return {"status": "Done", "led": "on", "pico_response": r.json()}
    except Exception as e:
        if "Max retries exceeded" in str(e) or "ConnectionTimeoutError" in str(e):
            return {"status": "Error!", "error": "Pico no disponible"}
        else:
            return {"status": "Error!", "error": str(e)}

# Ruta para apagar LED
@app.post("/led/off")
async def ledOff():
    idDispositivo = "raspi-001"
    websocket = activeConnections.get(idDispositivo)

    if websocket:
        try:
            await websocket.send_json({"command": "led_off"})  # Enviamos orden
            setLedState(False)
            return {"status": "Led apagado via websocket"}
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error al apagar led")

    ip = getPicoIp()

    if not ip:
        return {"status": "Error!", "error": "Raspberry no conectada"}

    try:
        r = requests.get(f"{ip}/led/off")  # Apagamos por HTTP
        setLedState(False)
        return {"status": "Done", "led": "off", "pico_response": r.json()}
    except Exception as e:
        if "Max retries exceeded" in str(e) or "ConnectionTimeoutError" in str(e):
            return {"status": "Error!", "error": "Pico no disponible"}
        else:
            return {"status": "Error!", "error": str(e)}