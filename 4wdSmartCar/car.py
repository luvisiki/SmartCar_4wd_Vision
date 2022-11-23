import wiringpi
import time

LOW = 0
LEFT_MOTOR_FONT = 28
LEFT_MOTOR_BACK = 29
RIGHT_MOTOR_FONT = 24
RIGHT_MOTOR_BACK = 25
LEFT_MOTOR_PWMcontorl = 27
RIGHT_MOTOR_PWMcontorl = 23
HIGH = 1

wiringpi.wiringPiSetup()

def Motor_init():
    wiringpi.pinMode(LEFT_MOTOR_FONT, LOW)
    wiringpi.pinMode(LEFT_MOTOR_BACK, LOW)
    wiringpi.pinMode(RIGHT_MOTOR_FONT, LOW)
    wiringpi.pinMode(RIGHT_MOTOR_BACK, LOW)
    wiringpi.softPwmCreate(LEFT_MOTOR_PWMcontorl, 0, 100)
    wiringpi.softPwmCreate(RIGHT_MOTOR_PWMcontorl, 0, 100)
    


def SmartCar_run(speed, delay):
    wiringpi.pinMode(LEFT_MOTOR_FONT, HIGH)
    wiringpi.pinMode(RIGHT_MOTOR_FONT, HIGH)
    wiringpi.pinMode(LEFT_MOTOR_BACK, LOW)
    wiringpi.pinMode(RIGHT_MOTOR_BACK, LOW)
    wiringpi.softPwmWrite(LEFT_MOTOR_PWMcontorl, speed)
    wiringpi.softPwmWrite(RIGHT_MOTOR_PWMcontorl, speed)
    time.sleep(delay)


def SmartCar_stop(speed, delay):
    wiringpi.pinMode(LEFT_MOTOR_FONT, LOW)
    wiringpi.pinMode(RIGHT_MOTOR_FONT, LOW)
    wiringpi.pinMode(LEFT_MOTOR_BACK, LOW)
    wiringpi.pinMode(RIGHT_MOTOR_BACK, LOW)
    wiringpi.softPwmWrite(LEFT_MOTOR_PWMcontorl, speed)
    wiringpi.softPwmWrite(RIGHT_MOTOR_PWMcontorl, speed)
    time.sleep(delay)


def SmartCar_turn_Left(speed1, speed2, delay):
    wiringpi.pinMode(LEFT_MOTOR_FONT, LOW)
    wiringpi.pinMode(RIGHT_MOTOR_FONT, HIGH)
    wiringpi.pinMode(LEFT_MOTOR_BACK, HIGH)
    wiringpi.pinMode(RIGHT_MOTOR_BACK, LOW)
    wiringpi.softPwmWrite(LEFT_MOTOR_PWMcontorl, speed2)
    wiringpi.softPwmWrite(RIGHT_MOTOR_PWMcontorl, speed1)
    time.sleep(delay)


def SmartCar_turn_Right(speed1, speed2, delay):
    wiringpi.pinMode(LEFT_MOTOR_FONT, HIGH)
    wiringpi.pinMode(RIGHT_MOTOR_FONT, LOW)
    wiringpi.pinMode(LEFT_MOTOR_BACK, LOW)
    wiringpi.pinMode(RIGHT_MOTOR_BACK, HIGH)
    wiringpi.softPwmWrite(LEFT_MOTOR_PWMcontorl, speed1)
    wiringpi.softPwmWrite(RIGHT_MOTOR_PWMcontorl, speed2)
    time.sleep(delay)


if __name__ == '__main__':
    try:
        wiringpi.wiringPiSetup()
        Motor_init()
        SmartCar_turn_Left(50, 30, 2)
    except KeyboardInterrupt:
        Motor_init()
#