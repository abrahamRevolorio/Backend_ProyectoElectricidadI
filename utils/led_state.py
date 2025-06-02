# Estado del LED (apagado por defecto)
led_state = {"on": False}

# Cambia el estado del LED
def setLedState(value: bool):
    led_state["on"] = value  # True = encendido, False = apagado

# Devuelve el estado actual del LED
def getLedState():
    return led_state["on"]  # Retorna True o False