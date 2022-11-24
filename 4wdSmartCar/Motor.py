import wiringpi
import time


class MotorControl:

    def __init__(self):
        wiringpi.wiringPiSetup()
        self.LEFT_MOTOR_FONT = 28
        self.LEFT_MOTOR_BACK = 29
        self.RIGHT_MOTOR_BACK = 25
        self.RIGHT_MOTOR_FONT = 24
        self.LEFT_MOTOR_PWMcontorl = 27
        self.RIGHT_MOTOR_PWMcontorl = 23

        self.SERVO_PIN = 4

        self.LOW = 0
        self.HIGH = 1

    def Motor_init(self):
        wiringpi.pinMode(self.LEFT_MOTOR_FONT, self.LOW)
        wiringpi.pinMode(self.LEFT_MOTOR_BACK, self.LOW)
        wiringpi.pinMode(self.RIGHT_MOTOR_FONT, self.LOW)
        wiringpi.pinMode(self.RIGHT_MOTOR_BACK, self.LOW)
        wiringpi.pinMode(self.SERVO_PIN, self.LOW)
        wiringpi.softPwmCreate(self.LEFT_MOTOR_PWMcontorl, 0, 100)
        wiringpi.softPwmCreate(self.RIGHT_MOTOR_PWMcontorl, 0, 100)
        wiringpi.softPwmCreate(self.SERVO_PIN, 0, 100)

    def SmartCar_run(self, speed, delay):
        wiringpi.pinMode(self.LEFT_MOTOR_FONT, self.HIGH)
        wiringpi.pinMode(self.RIGHT_MOTOR_FONT, self.HIGH)
        wiringpi.pinMode(self.LEFT_MOTOR_BACK, self.LOW)
        wiringpi.pinMode(self.RIGHT_MOTOR_BACK, self.LOW)
        wiringpi.digitalWrite(self.LEFT_MOTOR_FONT, self.HIGH)
        wiringpi.digitalWrite(self.RIGHT_MOTOR_FONT, self.HIGH)
        wiringpi.softPwmWrite(self.LEFT_MOTOR_PWMcontorl, speed)
        wiringpi.softPwmWrite(self.RIGHT_MOTOR_PWMcontorl, speed)
        time.sleep(delay)
    def SmartCar_back(self, speed, delay):
        wiringpi.pinMode(self.LEFT_MOTOR_FONT, self.LOW)
        wiringpi.pinMode(self.RIGHT_MOTOR_FONT, self.LOW)
        wiringpi.pinMode(self.LEFT_MOTOR_BACK, self.HIGH)
        wiringpi.pinMode(self.RIGHT_MOTOR_BACK, self.HIGH)
        wiringpi.digitalWrite(self.LEFT_MOTOR_BACK, self.HIGH)
        wiringpi.digitalWrite(self.RIGHT_MOTOR_BACK, self.HIGH)
        wiringpi.softPwmWrite(self.LEFT_MOTOR_PWMcontorl, speed)
        wiringpi.softPwmWrite(self.RIGHT_MOTOR_PWMcontorl, speed)
        time.sleep(delay)
    

    def SmartCar_turn_Left(self, speed1, speed2, delay):
        wiringpi.pinMode(self.LEFT_MOTOR_FONT, self.LOW)
        wiringpi.pinMode(self.RIGHT_MOTOR_FONT, self.HIGH)
        wiringpi.pinMode(self.LEFT_MOTOR_BACK, self.HIGH)
        wiringpi.pinMode(self.RIGHT_MOTOR_BACK, self.LOW)
        wiringpi.digitalWrite(self.RIGHT_MOTOR_FONT, self.HIGH)
        wiringpi.digitalWrite(self.LEFT_MOTOR_BACK, self.HIGH)
        wiringpi.softPwmWrite(self.LEFT_MOTOR_PWMcontorl, speed2)
        wiringpi.softPwmWrite(self.RIGHT_MOTOR_PWMcontorl, speed1)
        time.sleep(delay)

    def SmartCar_turn_Right(self, speed1, speed2, delay):
        wiringpi.pinMode(self.LEFT_MOTOR_FONT, self.HIGH)
        wiringpi.pinMode(self.RIGHT_MOTOR_FONT, self.LOW)
        wiringpi.pinMode(self.LEFT_MOTOR_BACK, self.LOW)
        wiringpi.pinMode(self.RIGHT_MOTOR_BACK, self.HIGH)
        wiringpi.digitalWrite(self.LEFT_MOTOR_FONT, self.HIGH)
        wiringpi.digitalWrite(self.RIGHT_MOTOR_BACK, self.HIGH)
        wiringpi.softPwmWrite(self.LEFT_MOTOR_PWMcontorl, speed1)
        wiringpi.softPwmWrite(self.RIGHT_MOTOR_PWMcontorl, speed2)
        time.sleep(delay)

    def ServoAngle(self, pos):
        wiringpi.pinMode(self.SERVO_PIN,self.HIGH)
        wiringpi.digitalWrite(self.SERVO_PIN,self.HIGH)
        wiringpi.softPwmWrite(self.SERVO_PIN, int(2.5 + 10 * pos/180))

    def Motor_stop(self):
        wiringpi.pinMode(self.LEFT_MOTOR_FONT, self.LOW)
        wiringpi.pinMode(self.RIGHT_MOTOR_FONT, self.LOW)
        wiringpi.pinMode(self.LEFT_MOTOR_BACK, self.LOW)
        wiringpi.pinMode(self.RIGHT_MOTOR_BACK, self.LOW)
        wiringpi.pinMode(self.SERVO_PIN, self.LOW)
            
# if __name__ == '__main__':
#     try:
#         wiringpi.wiringPiSetup()
#         Motor_init()
#         SmartCar_turn_Left(50, 30, 2)
#     except KeyboardInterrupt:
#         Motor_init()
#
