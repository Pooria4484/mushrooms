from .ui import *
from .config import*
from .setting import*
import uasyncio
import asocket
from save import *
from wifi import *
from math import fabs as abs

from wifi import ap
ap()
try:
    from . version import version as app_ver
except ImportError:
    print('no release it is debug')
from dht import DHT11
dh=DHT11(Pin(32))
server=asocket.Server()#socket server object
loop=uasyncio.get_event_loop()
tempTimer = Timer(0)
fanTimer = Timer(1)
mistTimer = Timer(2)
from gc import collect,mem_free
wdt = WDT(timeout=15000)  # enable wdt it with a timeout of 15s
ui=UI(oled,wdt)
print('MEM Free',mem_free())
collect()
print('MEM Free',mem_free())

buzzCnt=2
data=''
rx_flag=False#socket inbox handle flag
tTimerFlag=False#temp timer handle flag
mTimerFlag=False#mist timer handle flag
fTimerFlag=False#fan timer handle flag
def TempTimer(tempTimer):
    global tTimerFlag
    tTimerFlag=True
def FanTimer(fanTimer):
    global fTimerFlag
    fTimerFlag=True
def MistTimer(mistTimer):
    global mTimerFlag
    mTimerFlag=True
def SocketRx(Data):
    global rx_flag,data
    data=Data
    rx_flag=True


async def main():
    global tTimerFlag,mTimerFlag,fTimerFlag,rx_flag,data,buzzCnt
    tahandle=gettahe()#temp and hum auto handle with timer in case off sensor err
    err=0
    therr=False#temp and hum error flag
    cnt=0#main loop counter
    tcnt=0#main loop 10 ms counter
    therrcnt=0#th error counter
    tec=0#current temp var
    huc=0#current hum var
    hug=gethug()#goal hum
    teg=getteg()#goal temp
    tse=gettse()#temp system enable
    hse=gethse()#hum system enable
    gse=getgse()#gas system enable
    fte=getfte()#fan timer enable
    tte=gettte()#temp timer enable
    mte=getmte()#mist timer enable
    fton=getfton()#fan timer on time
    ftoff=getftoff()#fan timer off time
    mton=getmton()#mist timer on time
    mtoff=getmtoff()#mist timer off time
    tton=gettton()#temp timer on time
    ttoff=getttoff()#temp timer off time
    ttfast=getttfast()#temp timer fast time
    etse=getetse()#external temp sensor enabl
    ftrefresh=False #timers value changed
    ttrefresh=False
    mtrefresh=False
    thErrHandled=False
    errBuzzCnt=0 
    t=[0,0,0,0,0]
    tn=0
    print(rtc.datetime()[4:7])

    if tte:
        tempTimer.init(period=5000, mode=Timer.ONE_SHOT, callback=TempTimer)

    if mte:
        mistTimer.init(period=6000, mode=Timer.ONE_SHOT, callback=MistTimer)

    if fte:
        fanTimer.init(period=10000, mode=Timer.ONE_SHOT, callback=FanTimer)                                                


    up_cnt=0#up touch counter in 10ms
    down_cnt=0#down touch counter in 10ms
    ok_cnt=0#ok touch counter in 10ms
    menu_cnt=0#menu touch counter in 10ms
    page=0#ui page number
    item=0#ui item number
    mistOn=False
    mcnt=0
    while True:
        if mistOn:
            if mcnt==3600:
                if mist()==1:
                    print('moff',rtc.datetime()[4:7])
                    mist.off()
                    mcnt=0
            elif mcnt==400:
                if mist()==0:
                    mcnt=0
                    print('mon',rtc.datetime()[4:7])
                    mist.on()
        else:
            mist.off()        
        if up.value()==1:
            if up_cnt==5:
                buzzCnt=1
                if page==1:#main menu
                    if item<3:
                        item+=1
                    else:
                        item=0
                    ui.show_menu(page,item)
                elif page==2:#temperature page
                    if item<45:
                        item+=1
                    else:
                        item=11
                    ui.show_menu(page,int(item))            
                elif page==3:#temperature page
                    if item<95:
                        item+=3
                    else:
                        item=40
                    ui.show_menu(page,int(item))                                
                elif page==4:#fan page
                    if item==0:
                        item=1
                    else:
                        item=0    
                    ui.show_menu(page,int(item))    
                elif page==40 or page==41:
                    if item<=58:
                        item+=2    
                    else:
                        item=0        
                    ui.show_menu(page,int(item))        

            up_cnt+=1
        else:
            up_cnt=0


        if down.value()==1:
            if down_cnt==5:
                buzzCnt=1
                if page==1:#main menu
                    if item>0:
                        item-=1
                    else:
                        item=3    
                    ui.show_menu(page,item)
                elif page==2:#temperature page
                    if item>11:
                        item-=1
                    else:
                        item=45
                    ui.show_menu(page,int(item))                
                elif page==3:#hum page
                    if item>40:
                        item-=3
                    else:
                        item=95
                    ui.show_menu(page,int(item))                    
                elif page==4:#fan page    
                    if item==0:
                        item=1
                    else:
                        item=0    
                    ui.show_menu(page,item)    
                elif page==40 or page==41:
                    if item>=5:
                        item-=5    
                    else:
                        item=60    
                    ui.show_menu(page,item)        
            down_cnt+=1
        else:
            down_cnt=0


        if ok.value()==1:
            if ok_cnt==5:
                if page==0:
                    buzzCnt=1
                elif page==1:
                    buzzCnt=1
                    if item==0:
                        page=2
                        item=int(teg)
                    elif item==1:
                        page=3
                        item=int(hug)   
                    elif item==2:
                        page=4
                        item=0       
                    elif item==3:
                        save('update','True')
                        print('update','True')
                        page=0
                        item=0
                    ui.show_menu(page,item)
                elif page==2:
                    buzzCnt=2
                    teg=item
                    save('teg',str(int(item)))
                    print('teg',load('teg'),teg)
                    page=1
                    item=0
                    ui.show_menu(page,item)                
                elif page==3:
                    buzzCnt=2
                    hug=item
                    save('hug',str(int(item)))
                    print('hug',load('hug'),hug)
                    page=1
                    item=0
                    ui.show_menu(page,item)                                    
                elif page==4:
                    buzzCnt=2
                    if item==0:
                        page=40
                        item=fton
                    elif item==1:
                        page=41
                        item=ftoff
                    ui.show_menu(page,item)                                        

                elif page==40:
                    buzzCnt=2
                    fton=item
                    save('fton',str(int(item)))
                    print('fton',load('fton'),fton)
                    page=4
                    item=0
                    ui.show_menu(page,item)   

                elif page==41:
                    buzzCnt=2
                    ftoff=item
                    save('ftoff',str(item))
                    print('ftoff',load('ftoff'),ftoff)
                    page=4
                    item=0
                    ui.show_menu(page,item)       
                print('OK',page,item)
                
            ok_cnt+=1
        else:
            ok_cnt=0    

        
        if menu.value()==1:
            if menu_cnt==5:
                buzzCnt=1
                if page==0:
                    page=1
                    item=0
                else:
                    item=0
                    page=0    
                ui.show_menu(page,item)    
            menu_cnt+=1
        else:
            menu_cnt=0    

        if tcnt%3==0:
            
            if mtrefresh:
                mtrefresh=False
                mistTimer.deinit()
                if mte or (tahandle and therr):
                    mistOn=False
                    mistTimer.init(period=200, mode=Timer.ONE_SHOT, callback=MistTimer)
            if ttrefresh:
                ttrefresh=False
                tempTimer.deinit()
                if tte or (tahandle and therr):
                    cooler_motor.off()
                    cooler_water.off()
                    cooler_speed.off()
                    tempTimer.init(period=200, mode=Timer.ONE_SHOT, callback=TempTimer)
            if ftrefresh:
                ftrefresh=False
                fan.off()
                fanTimer.deinit()
                if fte:
                    fanTimer.init(period=200, mode=Timer.ONE_SHOT, callback=FanTimer)                                                
            cnt+=1      

            if cnt%7==0:
                server.send('*#wake@$\r\n')
                
            if dh!=None:
                etse=False
                if not etse:
                    try:
                        dh.measure()    
                        huc=dh.humidity()
                        t[0]=t[1]
                        t[1]=t[2]
                        t[2]=t[3]
                        t[3]=t[4]
                        t[4]=dh.temperature()
                        tn+=1
                        therr=False                    
                        if huc<=10:
                            therrcnt+=1    
                        if err==1:
                            err=0#resolve error
                            ui.set_err(0)
                        therrcnt=0
                    except Exception as e:
                        #print(e)
                        therrcnt+=1
                        if therrcnt>30:#wait for 30 cnt
                            therr=True                    
                            therrcnt=0    
                            if err==0:
                                ui.set_err(1)#show error
                                err=1
                    if tn>=5:
                        tn=0
                        dm=0
                        print(t)
                        print(dm,'abs1')
                        D43=abs(t[4]-t[3])
                        D41=abs(t[1]-t[4])
                        if D43>D41:
                            dm=D43
                        else:    
                            dm=D43
                        D42=abs(t[2]-t[4])
                        if D42>dm:
                            dm=D42
                        D40=abs(t[0]-t[4])
                        if D40>dm:
                            dm=D40
                        D31=abs(t[3]-t[1])
                        if D31>dm:
                            dm=D31
                        D32=abs(t[2]-t[3])
                        if D32>dm:
                            dm=D32
                        D30=abs(t[3]-t[0])
                        if D30>dm:
                            dm=D30
                        D21=abs(t[1]-t[2])
                        if D21>dm:
                            dm=D21
                        D20=abs(t[0]-t[2])
                        if D20>dm:
                            dm=D20
                        D10=abs(t[0]-t[1])
                        if D10>dm:
                            dm=D10
                        print(dm,'abs')
                        if  dm<2:
                            tec=(t[0]+t[1]+t[2]+t[3]+t[4])/5    
                    
                                    
                if not therr and therrcnt==0:#if temp and hum sensor has no error and errcnt is zero show tec and huc
                    ui.set_temp_hum(tec,huc)
     
            if therr:
                if errBuzzCnt>10:
                    errBuzzCnt=0
                    buzzCnt=3   
                errBuzzCnt+=1
                if not thErrHandled:
                    if tahandle:
                        thErrHandled=True
                        if (not mte) and hse:
                            mtrefresh=True
                            print('handle-hse')         
                        if (not tte) and tse:
                            ttrefresh=True  
                            print('handle-tse')         
            else:
                if thErrHandled:
                    if not mte:
                        mtrefresh=True
                    if not tte:
                        ttrefresh=True
                    thErrHandled=False    


            #iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
            if rx_flag:#handle messages from socket client
                rx_flag=False
                a = data.find('*#')
                b = data.find('@$')
                cmnd=''
                if a!=-1 and b>a:#check for start and end
                    cmnd=data[a+2:b]
                    #sssssssssssssssssssssssssssssssssssssssssssync
                    if cmnd.find('sync')!=-1:#check for sync command
                        buff='*#huc'+str(int(huc*10))+'hug'+str(hug)
                        if tec>9:
                            buff+='tec'+str(int(tec*10))+'teg'+str(teg)
                        else:
                            buff+='tec0'+str(int(tec*10))+'teg'+str(teg)    


                        if fton>9:    
                            buff+='fton'+str(fton)
                        else:
                            buff+='fton0'+str(fton)

                        if ftoff>9:    
                            buff+='ftoff'+str(ftoff)
                        else:
                            buff+='ftoff0'+str(ftoff)

                        if mton>9:    
                            buff+='mton'+str(mton)
                        else:
                            buff+='mton0'+str(mton)

                        if mtoff>9:
                            buff+='mtoff'+str(mtoff)
                        else:
                            buff+='mtoff0'+str(mtoff)    

                        if tton>9:    
                            buff+='tton'+str(tton)
                        else:
                            buff+='tton0'+str(tton)

                        if ttoff>9:
                            buff+='ttoff'+str(ttoff)
                        else:
                            buff+='ttoff0'+str(ttoff)

                        if ttfast>9:
                            buff+='ttfast'+str(ttfast)
                        else:
                            buff+='ttfast0'+str(ttfast)    
                        
                        buff2='RLH'+str(heater_valve.value())+str(heater_fan.value())+'M'+str(mist.value())+'F'+str(fan.value())+'C'+str(cooler_water.value())+str(cooler_motor.value())+str(cooler_speed.value())
                        buff+=buff2
                        
                        
                        if hse:
                            buff+='-HSE-'
                        else:
                            buff+='-HSD-'
                        
                        if tse:
                            buff+='-TSE-'
                        else:
                            buff+='-TSD-'

                        if tte:
                            buff+='-TTE-'
                        else:
                            buff+='-TTD-'

                        if mte:
                            buff+='-MTE-'
                        else:
                            buff+='-MTD-'
                                
                        if gse:
                            buff+='-GSE-'
                        else:
                            buff+='-GSD-'

                        if fte:
                            buff+='-FTE-'
                            
                        else:
                            buff+='-FTD-'


                        if etse:
                            buff+='-ESE-'
                            
                        else:
                            buff+='-ESD-'

                        if tahandle:
                            buff+='-TAHE-'
                        else:
                            buff+='-TAHD-'
                        

                        buff2="NOW"+str(rtc.datetime()[4:7]) 

                        buff+=buff2
                        buff2="ver"+app_ver
                        buff+=buff2+"@$\r\n"
                        server.send(buff)   
                        buzzCnt=1 
                    else:
                        print(cmnd)
                        buzzCnt=2

                    #system enabled and disable command
                    if cmnd.find('TSE')!=-1:#temp system
                        tse=settse(True)
                    if cmnd.find('TSD')!=-1:
                        tse=settse(False)   

                    if cmnd.find('HSE')!=-1:#hum system
                        hse=sethse(True)
                    if cmnd.find('HSD')!=-1:
                        hse=sethse(False)  

                    if cmnd.find('GSE')!=-1:#gas system
                        gse=setgse(True)
                    if cmnd.find('GSD')!=-1:
                        gse=setgse(False)  


                    if cmnd.find('TESE')!=-1:#temp external sensor
                        etse=setetse(True)  

                    if cmnd.find('TESD')!=-1:
                        etse=setetse(False)  

                    if cmnd.find('FTE')!=-1:#fan timer
                        fte=setfte(True)
                        ftrefresh=True

                    if cmnd.find('FTD')!=-1:
                        fte=setfte(False)  
                        ftrefresh=True
                        

                    if cmnd.find('TTE')!=-1:#temp timer
                        tte=settte(True)
                        ttrefresh=True

                    if cmnd.find('TTD')!=-1:
                        tte=settte(False)
                        ttrefresh=True



                    if cmnd.find('MTE')!=-1:#mist timer
                        mte=setmte(True)
                        mtrefresh=True

                    if cmnd.find('MTD')!=-1:
                        mte=setmte(False)
                        mtrefresh=True


                    if cmnd.find('UPDATE')!=-1:#app update enabled (OTA)
                        save('update','True')
                        print('update','True')


                    #change ap config
                    a = cmnd.find('APSSID')
                    b = cmnd.find('PASS')
                    c = cmnd.find('END')
                    if a!=-1 and b>a and c>b:
                        ssid=cmnd[a+6:b]
                        password=cmnd[b+4:c]
                        ap(s=ssid,p=password)
                        print('AP==>',ssid,password)


                    #change sta config
                    a = cmnd.find('STASSID')
                    b = cmnd.find('PASS')
                    c = cmnd.find('END')
                    if a!=-1 and b>a and c>b:
                        ssid=cmnd[a+7:b]
                        password=cmnd[b+4:c]
                        sta(s=ssid,p=password)
                        print('STA==>',ssid,password)

                    #goal hum
                    a = cmnd.find('hug')
                    if a!=-1:
                        hug=sethug(a,cmnd)
                        
                    #goal temp
                    a = cmnd.find('teg')
                    if a!=-1:
                        teg=setteg(a,cmnd)

                    #external hum sensor hum
                    a = cmnd.find('huc')
                    if a!=-1:
                        if etse:
                            try:
                                huc=int(cmnd[(a+3):(a+6)])/10
                            except ValueError:
                                pass
                        
                    #external temp sensor temp
                    a = cmnd.find('tec')
                    if a!=-1:
                        if etse:
                            try:
                                tec=int(cmnd[(a+3):(a+6)])/10
                            except ValueError:
                                pass


                    #timers values change
                    a = cmnd.find('fton')
                    if a!=-1:
                        fton=setfton(a,cmnd)
                        ftrefresh=True
                        

                    a = cmnd.find('ftoff')
                    if a!=-1:
                        ftoff=setftoff(a,cmnd)
                        ftrefresh=True


                    a = cmnd.find('mton')
                    if a!=-1:
                        mton=setmton(a,cmnd)
                        mtrefresh=True
                        

                    a = cmnd.find('mtoff')
                    if a!=-1:
                        mtoff=setmtoff(a,cmnd)
                        mtrefresh=True

                        

                    a = cmnd.find('tton')
                    if a!=-1:
                        tton=settton(a,cmnd)
                        ttrefresh=True
                        

                    a = cmnd.find('ttoff')
                    if a!=-1:
                        ttoff=setttoff(a,cmnd)                        
                        ttrefresh=True


                    a = cmnd.find('ttfast')
                    if a!=-1:
                        ttfast=setttfast(a,cmnd)
                        ttrefresh=True
                        


                    a = cmnd.find('TAHE')
                    if a!=-1:
                        tahandle=settahe(True)

                    a = cmnd.find('TAHD')
                    if a!=-1:
                        tahandle=settahe(False)    
                        

                    a = cmnd.find('ver')
                    if a!=-1:    
                        buff='app ver==>'+app_ver+'\r\n'
                        server.send(buff)                


            if tcnt%10==0:
                if tse and (not tte):#if temp system enabled and temp timer disabled
                    if not therr:#if temp has no err
                        if tec>=(teg+3.0):#vary very hot
                            print('very hot')
                            if cooler_speed()==0 or cooler_water()==0:
                                cooler_speed(1)
                                cooler_water(1)
                                cooler_motor(1)
                                
                        elif tec>=(teg+1.0):#vary very hot
                            print('hot') 
                            if cooler_water()==0 or cooler_speed()==1:
                                cooler_speed(0)
                                cooler_water(1)
                                cooler_motor(1)  
                                     
                        elif tec<=(teg-1.0):#vary very hot
                            print('cold') 
                            if cooler_water()==1:
                                cooler_speed(0)
                                cooler_water(0)
                                cooler_motor(0)   
                #         if tec>(teg+3.0):#vary very hot


                #             if(heater_fan.value()==1):
                #                 heater_fan.off()
                #                 # await uasyncio.sleep_ms(250)
                #                 heater_valve.off()
                #                 # await uasyncio.sleep_ms(250)
                            
                #             if(cooler_water.value()!=1):
                #                 cooler_water.on()
                #                 # await uasyncio.sleep_ms(250)
                #                 cooler_motor.on()
                #             if(cooler_speed.value()!=1):                    
                #                 # await uasyncio.sleep_ms(250)
                #                 cooler_speed.on()


                #         elif tec>(teg+1.5):#ver hot

                #             if(heater_fan.value()==1):
                #                 heater_fan.off()
                #                 # await uasyncio.sleep_ms(250)
                #                 heater_valve.off()
                #                 # await uasyncio.sleep_ms(250)
                                            
                #             if(cooler_motor.value()!=1):
                #                 cooler_water.on()
                #                 # await uasyncio.sleep_ms(250)
                #                 cooler_motor.on()
                #                 # await uasyncio.sleep_ms(250)
                #             if(cooler_speed.value()==1):                        
                #                 cooler_speed.off()


                #         elif tec>(teg+0.8):#medium
                #             if(heater_fan.value()==1):
                #                 heater_fan.off()
                #                 # await uasyncio.sleep_ms(250)
                #                 heater_valve.off()
                #                 # await uasyncio.sleep_ms(250)        

                #         elif tec<(teg-2.0):#very cold
                #             if(heater_fan.value()!=1):
                #                 heater_fan.on()
                #                 # await uasyncio.sleep_ms(250)
                #                 heater_valve.on()
                #                 # await uasyncio.sleep_ms(250)


                #             if(cooler_motor.value()==1):
                #                 cooler_water.off()
                #                 # await uasyncio.sleep_ms(250)
                #                 cooler_motor.off()
                #                 # await uasyncio.sleep_ms(250)
                #             if(cooler_speed.value()==1):                        
                #                 cooler_speed.off()


                #         elif tec<(teg-1.0):#cold
                #             if(cooler_motor.value()==1):
                #                 cooler_water.off()
                #                 # await uasyncio.sleep_ms(250)
                #                 cooler_motor.off()
                #                 # await uasyncio.sleep_ms(250)
                #             if(cooler_speed.value()==1):                        
                #                 cooler_speed.off()            
                #     else:#temp err
                #         if (not tahandle):#temp error auto handle
                #             cooler_motor.off()
                #             cooler_speed.off()
                #             cooler_water.off()
                #             heater_valve.off()
                #             heater_fan.off()
                # else:#temp system off
                #     if not tte:
                #         cooler_motor.off()
                #         cooler_speed.off()
                #         cooler_water.off()
                #         heater_valve.off()
                #         heater_fan.off()


                if hse:#hum system enabled and mist timer disabled
                    if not mte:
                        if not therr:#no mist err
                            if huc<hug-10:
                                #mist.on()
                                mistOn=True
                            elif huc>hug+10:
                                #mist.off()    
                                mistOn=False
                        else:
                            if not tahandle:
                                mistOn=False      
                else:
                    if not (mte or tahandle):
                        mist.off()


                if gse:#gas system enabled
                    pass
                else:
                    if not fte:#fan timer disabled
                        fan.off()

            if(mTimerFlag):
                mTimerFlag=False
                if mte or (tahandle and therr):
                    mistOn=not mistOn
                    #mist(not mist.value())
                    if mistOn:
                        mt=mton
                    else:
                        mt=mtoff   
                    mistTimer.init(period=60000*mt, mode=Timer.ONE_SHOT, callback=MistTimer)
                    print('mTimer reached','mist',mist.value(),rtc.datetime()[4:7])
            
            if(fTimerFlag):
                fTimerFlag=False
                if(fte):
                    fan(not fan.value())
                    print('fTimer reached',rtc.datetime()[4:7],'fan',fan.value())
                    if fan.value()==1:
                        ft=fton
                    else:
                        ft=ftoff
                    fanTimer.init(period=ft*60000, mode=Timer.ONE_SHOT, callback=FanTimer)

            if(tTimerFlag):
                tTimerFlag=False
                if tte or (tahandle and therr):
                    if cooler_water.value()==0:
                        cooler_water(1)
                        cooler_motor(1)
                        if ttfast!=0:
                            cooler_speed(1)
                            tt=ttfast
                        else:
                            cooler_speed(0)    
                            tt=tton
                    else:
                        if ttfast!=0:
                            if cooler_speed.value()==1:
                                tt=tton
                            else:
                                tt=ttoff        
                                cooler_motor(0)
                                cooler_water(0)
                        else:
                            tt=ttoff
                            cooler_motor(0)
                            cooler_water(0)                            
                        cooler_speed(0)        
                    tempTimer.init(period=tt*60000, mode=Timer.ONE_SHOT, callback=TempTimer)
                    print('tTimer reached','water',cooler_water.value(),'motor',cooler_motor.value(),'speed',cooler_speed.value(),rtc.datetime()[4:7])


        tcnt+=1
        mcnt+=1
        await uasyncio.sleep_ms(25)


async def BuzzTask():
    global buzzCnt
    while True:
        if buzzCnt>0:
            if buzz.value()==0:
                buzz.on()
            else:
                buzzCnt-=1
                buzz.off()
        await uasyncio.sleep_ms(75)


server.set_rlistener(SocketRx)
loop.create_task(server.run(loop))
loop.create_task(ui.Run())
loop.create_task(BuzzTask())
try:
    loop.run_until_complete(main())
except KeyboardInterrupt:
    print('Interrupted')
finally:
  server.close()        
