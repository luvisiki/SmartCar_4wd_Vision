import wiringpi
import time


class SmartCar_contorl:
    def __init__(self) -> None:
        pass

INPUT = 0
OUTPUT = 1
PWM_OUTPUT = 2
GPIO_CLOCK = 3
SOFT_PWM_OUTPUT = 4
SOFT_TONE_OUTPUT = 5
PWM_TONE_OUTPUT = 6
LOW = 0
HIGH = 1

PWM_PIN_LEFT = 28
PWM_PIN_RIGHT = 29
PWM_PIN_LEFT_ture = 27

wiringpi.wiringPiSetup()
# wiringpi.pwmSetMode(2)
# wiringpi.pinMode(PWM_PIN, 1)
# print("pwm:",wiringpi.digitalRead(PWM_PIN))
wiringpi.pinMode(PWM_PIN_LEFT, 1)
wiringpi.pinMode(PWM_PIN_RIGHT, 1)
wiringpi.softPwmCreate(PWM_PIN_LEFT_ture,0,100)
# wiringpi.softPwmCreate(PWM_PIN_LEFT,0,100)
# wiringpi.softPwmCreate(PWM_PIN_RIGHT,0,100)
# print("28_left_font:",wiringpi.digitalRead(28))
try:
    while 1:
        # for speed in range(0, 80):
        # wiringpi.digitalWrite(28, 0)
        # wiringpi.digitalWrite(29, 0)
        for speed in range(40,50):
            wiringpi.softPwmWrite(PWM_PIN_LEFT_ture,speed)
            wiringpi.digitalWrite(PWM_PIN_LEFT, 1)
            # wiringpi.delay(100)
            # wiringpi.digitalWrite(PWM_PIN_LEFT, 0)
            # wiringpi.delay(100)
            # wiringpi.digitalWrite(PWM_PIN_RIGHT, 1)
            # wiringpi.delay(100)
            # wiringpi.digitalWrite(PWM_PIN_RIGHT, 0)
            wiringpi.delay(50)
            time.sleep(5)
            print(speed)
        # wiringpi.softPwmWrite(PWM_PIN_RIGHT,50)
        # wiringpi.delay(50)
        # for speed in range(1000, 0, -1):
        #     wiringpi.pwmWrite(PWM_PIN, speed)
        #     wiringpi.delay(1)
except KeyboardInterrupt:
    pass
wiringpi.digitalWrite(PWM_PIN_RIGHT,0)
wiringpi.digitalWrite(PWM_PIN_LEFT,0)