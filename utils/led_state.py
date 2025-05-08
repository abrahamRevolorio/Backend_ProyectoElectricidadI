led_state = {"on": False}

def setLedState(value: bool):
    led_state["on"] = value

def getLedState():
    return led_state["on"]