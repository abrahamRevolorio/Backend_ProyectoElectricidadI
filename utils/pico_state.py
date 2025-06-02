# IP actual del Pico (vacía al inicio)
picoIp = None

# Guarda la IP del Pico
def setPicoIp(ip: str):
    global picoIp
    picoIp = ip  # Asigna la IP recibida

# Devuelve la IP guardada
def getPicoIp():
    print(picoIp)  # Muestra la IP en consola
    return picoIp  # Retorna la IP