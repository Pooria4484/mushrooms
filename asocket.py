import usocket as socket
import uasyncio as asyncio
import uselect as select
import gc
class Server(object):
    def __init__(self, port=39810,max=1): 
        self.port=port
        self.max=max
        self.client_out_box=[]
        for x in range(max):
            self.client_out_box.append('ss')
    def send(self,msg):
        for x in range (self.max):
            self.client_out_box[x]=msg
    async def run(self, loop):#run socket
        addr = socket.getaddrinfo('0.0.0.0', self.port, 0, socket.SOCK_STREAM)[0][-1]
        s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # server socket
        s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s_sock.bind(addr)
        s_sock.listen(0)
        self.socks = [s_sock]
        poller = select.poll()
        poller.register(s_sock, select.POLLIN)
        self.client_cnt = 0  # For user feedback
        while True:
            gc.collect()
            if self.client_cnt<self.max:
                res = poller.poll(1)
                if res :
                    c_sock, _ = s_sock.accept()
                    loop.create_task(self.run_client(c_sock, self.client_cnt,loop))
                    self.client_cnt +=1
            await asyncio.sleep_ms(120)
    async def run_client(self, sock, cid,loop):
        self.socks.append(sock)
        t=self.send_task(sock,cid)
        task=loop.create_task(t)
        sreader = asyncio.StreamReader(sock)
        inbox=bytearray()
        print('Got connection from client', cid)
        try:
            while True:
                res = await sreader.read(1)
                if res == b'':
                    raise OSError
                else:
                    inbox.append(res[0])
                    if str(res,'utf-8')=='\n':
                        #print(inbox)
                        self.lis(str(inbox,'utf-8'))
                        inbox=bytearray()
        except OSError:
            task.cancel()
            print('err')
        sock.close()     
        print('Client {} disconnect.'.format(cid))    
        self.client_cnt-=1
        self.socks.remove(sock)
        
    async def send_task(self, sock, cid):
        swriter = asyncio.StreamWriter(sock, {})
        while True:
            try:
                if self.client_out_box[cid]!='':
                    await swriter.awrite(self.client_out_box[cid])
                    self.client_out_box[cid]=''
            except OSError:
                sock.close()
                print('err')
            await  asyncio.sleep_ms(120)       
    def close(self):
        for sock in self.socks:
            sock.close()
    def set_rlistener(self,lis):
        self.lis=lis
    def is_busy(self):
        return self.busy

