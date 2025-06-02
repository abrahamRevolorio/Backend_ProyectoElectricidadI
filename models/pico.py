from pydantic import BaseModel  # Base para modelos de validación

# Modelo de datos del dispositivo Pico
class Pico(BaseModel):
    ip: str  # IP del dispositivo en formato texto