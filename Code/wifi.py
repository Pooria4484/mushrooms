from network import WLAN ,AP_IF,STA_IF
from save import save,load
def sta(s="msb",p="12345678",h=False):
    save('SSID',s)
    save('PASS',p)
    sta_if=WLAN(STA_IF)
    sta_if.active(True)
    sta_if.connect(s,p) 
    print(sta_if.ifconfig())
def son():
    s=load('SSID')
    p=load('PASS')
    sta_if=WLAN(STA_IF)
    sta_if.active(True)
    sta_if.connect(s,p) 
def soff():
    sta_if=WLAN(STA_IF)
    sta_if.active(False)
    
def ap(s="MSB80201001",p="msb-co.ir"):
    save('ssid',s)
    save('pass',p)
    ap_if=WLAN(AP_IF)
    ap_if.active(True)
    ap_if.config(authmode=4,password=p)
    ap_if.config(essid=s)
    ap_if.config(max_clients=2)
    print(ap_if.ifconfig())
def aon():
    ap_if=WLAN(AP_IF)
    ap_if.active(True)
def aoff():
    ap_if=WLAN(AP_IF)
    ap_if.active(False)    
def isConected():
    sta_if=WLAN(STA_IF)
    return sta_if.isconnected()
def ifconfig():
    sta_if=WLAN(STA_IF)
    return sta_if.ifconfig()