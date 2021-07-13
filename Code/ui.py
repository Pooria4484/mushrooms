import uasyncio
import framebuf
import btree
class UI:    
    def _show_image(self,path,w,h,x,y):
        try:
            f=open(path)
            s=f.read(int((w*h)/8))
            arr=bytearray(s)
            f.close()
            fbuf = framebuf.FrameBuffer(arr, w, h, framebuf.MONO_VLSB)
            self.oled.blit(fbuf,x,y)
        except OSError:
            pass
    def _show_err(self,n):
        path='dgt/err'
        if self.type==2:
            self._show_image(path,128,64,0,10)
        else:
            self._show_image(path,128,64,0,0)
        d=int(n/10)%10
        path='dgt/d'+str(d)
        if self.type==2:
            self._show_image(path,26,40,78,22)
        else:    
            self._show_image(path,26,40,78,12)

        d=int(n%10)
        path='dgt/d'+str(d)
        if self.type==2:
            self._show_image(path,26,40,104,22)
        else:
            self._show_image(path,26,40,104,12)
        
        self.oled.show()
    def _show_time(self,h,m):
        self.oled.fill(0)
        if self.type!=2:
            self._show_image('dgt/dd',12,24,60,20)
        else:
            self._show_image('dgt/dd',12,24,60,27)

        d=int(h/10)%10
        path='dgt/d'+str(d)
        if self.type!=2:
            self._show_image(path,26,40,0,5)
        else:    
            self._show_image(path,26,40,0,15)

        d=int(h%10)
        path='dgt/d'+str(d)
        if self.type!=2:
            self._show_image(path,26,40,28,5)
        else:
            self._show_image(path,26,40,28,15)
        
        
        d=int(m/10)%10
        path='dgt/d'+str(d)
        if self.type!=2:
            self._show_image(path,26,40,75,5)
        else:
            self._show_image(path,26,40,75,15)


        d=int(m%10)        
        path='dgt/d'+str(d)
        if self.type!=2:
            self._show_image(path,26,40,103,5)
        else:
            self._show_image(path,26,40,103,15)
        self.oled.show()
    def set_err(self,n):
        if n!=0:
            self.err=True
            self.enum=n
            self.ready=False
            self.working=False
        else:
            self.err=False
            self.ready=True
    def __init__(self,oled):
        #self.wdt=wdt
        self.oled=oled
        self.err=False
        self.ready=False
        self.working=False
    async def Run(self):
        self.type=2
        self._show_image('dgt2/logo',128,64,0,3)
        self.oled.show()
        await uasyncio.sleep_ms(4000)
        while True:
            await uasyncio.sleep_ms(300)
