import uasyncio
import asocket
from config import*
try:
    from version import version
except ImportError:
    print('no release it is debug')
    pass
led=Pin(2,Pin.OUT)
server=asocket.Server()
loop=uasyncio.get_event_loop()
class Main:
    async def Run():
        while True:
            led(not led())    
            await uasyncio.sleep_ms(250)
main=Main
loop.create_task(server.run(loop))
loop.create_task(ui.Run())
try:
    loop.run_until_complete(Main.Run())
except KeyboardInterrupt:
    print('Interrupted')
finally:
  server.close()        
            
