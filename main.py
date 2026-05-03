import pyb
import upcd8544
from machine import SPI,Pin
from pyb import UART
from sht20 import SHT20
import time
jishu_0=0
ds = SHT20(1)
leds = [pyb.LED(i) for i in range(1,5)]
SPI = pyb.SPI(1)
RST = pyb.Pin('X20')
CE = pyb.Pin('X19')
DC = pyb.Pin('X18')
LIGHT = pyb.Pin('X17')
lcd_5110 = upcd8544.PCD8544(SPI, RST, CE, DC, LIGHT)
N1 = Pin('Y6', Pin.OUT_PP)
print('设备启动中...')
lcd_5110.lcd_write_string('starting...',0,0)
N1.low()
pyb.delay(2000)
N1.high()
pyb.delay(10000)
u2 = UART(4, 115200,timeout=100)
def DataConver(str_,flag):
    wei_=float(str_)/100
    wei_arr=str(wei_).split('.')
    val_=100000
    if flag==0:
        val_=10000
    wei_arr[1]=str(float(wei_arr[1])/60*val_).replace('.','')
    weidu=wei_arr[0]+'.'+wei_arr[1]
    return weidu
print('设备启动成功')
lcd_5110.lcd_write_string('Start successfully.',0,0)
while True:
    print('**********')
    print('设备数据')
    pyb.LED(1).on()
    time.sleep(0.05)
    pyb.LED(1).off()
    u2.write('AT+GPSLOC=1\r\n')
    pyb.delay(500)
    _dataRead=u2.read()
    pyb.delay(1000)
    u2.write('AT+GPSLOC=0\r\n')
    pyb.delay(200)
    _dataRead=u2.read()
    if _dataRead!=None:
        if 60<len(_dataRead)<70:
            _dataRead = _dataRead.decode('utf-8')
            _dataRead1=_dataRead.split(',')
            if len(_dataRead1)>4:
                weidu=_dataRead1[1]
                WD=DataConver(weidu,0)
                jingdu=_dataRead1[2]
                JD=DataConver(jingdu,1)
                gaodu=_dataRead1[3]
                shijian_zhong=_dataRead1[4]
    if jishu_0==0:
        lcd_5110.lcd_write_string("              ",0,0)
        jishu_0=1
    else:
        pass
    lcd_5110.lcd_write_string(str(JD),0,0)
    lcd_5110.lcd_write_string(str(WD),0,1)
    lcd_5110.lcd_write_string(str(gaodu),0,2)
    lcd_5110.lcd_write_string(str(shijian_zhong),0,3)
    print('经度=',str(JD))
    print('纬度=',str(WD))
    print('高度=',str(gaodu))
    print('时间=',str(shijian_zhong))
    pyb.LED(3).on()
    time.sleep(0.05)
    pyb.LED(3).off()
    ads = pyb.ADC(Pin('Y12'))
    a=ads.read()
    a=a/100
    a=33-a
    H=ds.TEMP()
    S=ds.TEMP1()
    H=125*H/256-6
    S=175.72*S/256-46.85
    lcd_5110.lcd_write_string(str(S),0,4)
    lcd_5110.lcd_write_string(str(H),0,5)
    print('温度=',str(S))
    print('湿度=',str(H))
#qingx编写