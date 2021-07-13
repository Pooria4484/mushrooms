
from wifi import*
from save import*
print('OTA-UPDATER')
def connectToWifiAndUpdate():
    print('connectToWifiAndUpdate')
    import time,machine, wifi, gc
    try:
        flag=load(b"update")
    except KeyError:
        flag=b"False"
        save(b"update",flag)
    print('update-->',flag)    
    if flag==b"True":
        flag=b"False"
        save(b"update",flag)
        aoff()        
        time.sleep_ms(200)        
        if ifconfig()[0]=='0.0.0.0':            
            print('connectToWifiAndUpdate')
            try:
                son()
            except OSError:
                pass
            print('waiting for connection...')
            while ifconfig()[0]=='0.0.0.0':
                print(ifconfig())
                time.sleep(1)
        from app.ota_updater import OTAUpdater
        if(ifconfig()[0]!='0.0.0.0'):
            print('network config:', ifconfig())
            token='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'
            #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
            otaUpdater = OTAUpdater('https://github.com/Pooria4484/esp8266-wmOLED', main_dir='app',headers={'Authorization': 'token {}'.format(token)})
            hasUpdated=None
            #try:
            hasUpdated = otaUpdater.install_update_if_available()
            #except OSError:
                #print('osErr')
                #pass     
            if hasUpdated:
                machine.reset()
                save(b"update",b"False")
            else:
                del(otaUpdater)
        print('DONE')
    gc.collect()
def startApp():
    import app.app
connectToWifiAndUpdate()
startApp()
