from fastapi import HTTPException
from typing import Optional

def validarIp(ip: Optional[str]):

    if not ip:
        raise HTTPException(status_code=400, detail="Ip no proporcionada")
    
    if not ip.startswith("http://") and not ip.startswith("https://"):
        ip = "http://" + ip

    return ip