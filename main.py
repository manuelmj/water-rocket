# Write your code here :-)
import machine
from machine import I2C, Pin , PWM
from time import sleep_ms
from mpu_6050 import accel


pin13 = Pin(13 , Pin.OUT)
pin23 = Pin(23 , Pin.IN, Pin.PULL_DOWN)
led =  Pin(2, Pin.OUT)
pin36 = Pin(26, Pin.OUT)
pwm = PWM(pin13) #initializing the PWM for ESP32
buzzer = PWM(pin36)
i2c = I2C(scl=Pin(22), sda=Pin(21))     #initializing the I2C method for ESP32

pwm.freq(50)
pwm.duty(0)

buzzer.duty(0)

mpu = accel(i2c)

state = 0
degree = 80
led.value(0)

while(True):
    #print(cuenta)
    #sleep_ms(500)

    if pin23.value() == 1 and state == 0:
        sleep_ms(500)
        state = True
        led.value(1)
        buzzer.duty(255)
        sleep_ms(1000)
        buzzer.duty(0)

    elif pin23.value() == 1 and state == 1:
        sleep_ms(500)
        state = False
        led.value(0)

    if state == True :
        zx_permition_degrees = (mpu.pitch_zx() < -degree) or (mpu.pitch_zx() > degree)
        zy_permition_degrees = (mpu.pitch_zy() < -degree) or (mpu.pitch_zy() > degree)

        if zx_permition_degrees or zy_permition_degrees:
            #sleep_ms(500)
           # if zx_permition_degrees or zy_permition_degrees:
            pwm.duty(130)
            print("abriendo paracaidas")
            print(mpu.pitch_zx(), mpu.pitch_zy())





        else:
            pwm.duty(20)


