picoIp = None

def setPicoIp(ip: str):
    global picoIp
    picoIp = ip

def getPicoIp():
    print(picoIp)
    return picoIp