from mfrc522 import MFRC522
from machine import Pin, PWM
from machine import SPI
import network, time
from utelegram import *
from utime import sleep, sleep_ms
import ujson
import ufirebase as firebase

def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True


if conectaWifi ("SSID", "Password"):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
      
    firebase.setURL("https://kingsecurity-e260e-default-rtdb.firebaseio.com/")
 
else:
    print ("Imposible conectar")
    miRed.active (False)

servo = PWM(Pin(26), freq=50)

def map_s(x):
    return int((x - 0) * (125- 25) / (180 - 0) + 25)
"do_connect()"

TOKEN= '5623759506:AAHPNx9Bg-iW3n3igSSizr1to3QgyQZFnvY'
bot = Bot(TOKEN)

ledRojo  =     Pin(14,Pin.OUT)
ledVerde =     Pin(13,Pin.OUT)
ledAzul  =     Pin(12,Pin.OUT)

def leds(a,b,c):
  ledRojo(not a)
  ledVerde(not b)
  ledAzul(not c)
spi = SPI(2, baudrate=2500000, polarity=0, phase=0)

spi.init()
1
rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)
leds(1,1,0)
print("Place card")



while True:
    
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
    
     
        if stat == rdr.OK:
            print("Verificando")
            card_id = "0x%02x%02x%02x%02x" %(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
            print("UID:", card_id)
            message={"valor_a":"Puerta Cerrada"}
            firebase.put("Puerta/Estado de la puerta",message, bg=0)

            if card_id == "0x880453a5":
                
                bot.send_message('685356973',"estas intentando ingresar al DC, confirma con 1 para si o 2 para no")
                
                @bot.add_message_handler('1')
                def help(update):
                    leds(0,1,0)
                    update.reply("Acceso garantizado")
                    angulo= 0
                    m= map_s(angulo)
                    servo.duty(m)
                    message={"valor_a":"Puerta Abierta","valor_c":True}
                    firebase.put("Puerta/Estado de la puerta",message, bg=0)
                    sleep(5)
                    angulo= 90
                    m= map_s(angulo)
                    servo.duty(m)
                    message={"valor_a":"Puerta Cerrada","valor_c":False}
                    firebase.put("Puerta/Estado de la puerta",message, bg=0)
                    leds(1,1,0)
                              
                @bot.add_message_handler('2')
                def help(update):
                    leds(1,0,0)
                    update.reply("Acceso denegado")
                    message={"valor_a":"Acceso Denegado","valor_c":False}
                    firebase.put("Puerta/Estado de la puerta",message, bg=0)
                    leds(1,1,0)
                
                                              
                bot.start_loop()
 
            else:
                leds(1,0,0)                              
                print(" Access Denied! ")
                message={"valor_a":"Acceso Denegado","valor_c":False}
                firebase.put("Puerta/Estado de la puerta",message, bg=0)
                leds(1,1,0)
                
     