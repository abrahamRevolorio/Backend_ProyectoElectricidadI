from fastapi import HTTPException
from typing import Optional

# Valida y ajusta una IP recibida
def validarIp(ip: Optional[str]):

    # Si no hay IP, error 400
    if not ip:
        raise HTTPException(status_code=400, detail="Ip no proporcionada")
    
    # Si no empieza con http o https, se le agrega
    if not ip.startswith("http://") and not ip.startswith("https://"):
        ip = "http://" + ip

    return ip  # Retorna la IP ya validada