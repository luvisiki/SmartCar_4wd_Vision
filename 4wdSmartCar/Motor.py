import wiringpi
import time
import RPi.GPIO as GPIO



class MotorControl:
    '''
    @@@@@@@@
    @@ Developer: Han Cao , id:202244060101
    @@ Class name: MotorControl 
    @@ Input: none
    @@ output:fuction
    @@ Description:Class encapsulates the initialization function of the motor, the variate drive function, and the ultrasonic distance measurement function.
    @@@@@@@@
    '''
    def __init__(self):
        wiringpi.wiringPiSetup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.LEFT_MOTOR_FONT = 28
        self.LEFT_MOTOR_BACK = 29
        self.RIGHT_MOTOR_BACK = 25
        self.RIGHT_MOTOR_FONT = 24
        self.LEFT_MOTOR_PWMcontorl = 27
        self.RIGHT_MOTOR_PWMcontorl = 23

        # using BCM coder
        self.EchoPin = 0   # ULsonic Send
        self.TrigPin = 1   # ULsonic Receive
        # self.SERVO_PIN = 4

        self.LOW = 0
        self.HIGH = 1

    def Motor_init(self):
        '''
        @@@@@@@@
        @@ Developer: Han Cao, id:202244060101
        @@ Fuction name: Motor_init
        @@ Input: none
        @@ output: none
        @@ Description: Using wiringpi Initialization Motor Pin and setup softPwm. Using GPIO Initialization Ultrasonic PIN.
        @@@@@@@@
        '''
        wiringpi.pinMode(self.LEFT_MOTOR_FONT, self.LOW)
        wiringpi.pinMode(self.LEFT_MOTOR_BACK, self.LOW)
        wiringpi.pinMode(self.RIGHT_MOTOR_FONT, self.LOW)
        wiringpi.pinMode(self.RIGHT_MOTOR_BACK, self.LOW)
        GPIO.setup(self.EchoPin, GPIO.IN)
        GPIO.setup(self.TrigPin, GPIO.OUT)
        wiringpi.softPwmCreate(self.LEFT_MOTOR_PWMcontorl, 0, 100)
        wiringpi.softPwmCreate(self.RIGHT_MOTOR_PWMcontorl, 0, 100)
        

    def ultarsonic_ExaminDistant(self):
        '''
        @@@@@@@@
        @@ Developer: Han Cao, id:202244060101
        @@ Fuction name: ultarsonic_ExaminDistant
        @@ Input: none
        @@ output: Distance measurements
        @@ Description: Use the ultrasonic principle to detect the high level time of the EchoPin time.Then use the formula to calculate the distance from the obstacle.
        @@@@@@@@
        '''
        GPIO.output(self.TrigPin, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(self.TrigPin, GPIO.LOW)
        while not GPIO.input(self.EchoPin):
            pass
        t1 = time.time()
        while GPIO.input(self.EchoPin):
            pass
        t2 = time.time()
        # print ("distance is %d " % (((t2 - t1) * 340 / 2) * 100))
        time.sleep(0.01)
        return int(((t2 - t1) * 340 / 2) * 100)

    def SmartCar_run(self, speed, delay):
        '''
        @@@@@@@@
        @@ Developer: Han Cao, id:202244060101
        @@ Fuction name: SmartCar_run
        @@ Input: Para1-> speed Para2->delay time
        @@ Description: drive the pin of motor and make 4WD car go straight
        @@@@@@@@
        '''
        wiringpi.pinMode(self.LEFT_MOTOR_FONT, self.HIGH)
        wiringpi.pinMode(self.RIGHT_MOTOR_FONT, self.HIGH)
        wiringpi.pinMode(self.LEFT_MOTOR_BACK, self.LOW)
        wiringpi.pinMode(self.RIGHT_MOTOR_BACK, self.LOW)
        wiringpi.digitalWrite(self.LEFT_MOTOR_FONT, self.HIGH)
        wiringpi.digitalWrite(self.RIGHT_MOTOR_FONT, self.HIGH)
        wiringpi.softPwmWrite(self.LEFT_MOTOR_PWMcontorl, speed)
        wiringpi.softPwmWrite(self.RIGHT_MOTOR_PWMcontorl, speed)
        time.sleep(delay)
        self.Motor_stop()

    def SmartCar_back(self, speed1, speed2, delay):
        '''
        @@@@@@@@
        @@ Developer: Han Cao, id:202244060101
        @@ Fuction name: SmartCar_back
        @@ Input: Para1-> speed1(left motor) Para2->speed2(right motor) Para3->delay time
        @@ Description: drive the pin of motor and make 4WD car Stand back. 
        @@@@@@@@
        '''
        wiringpi.pinMode(self.LEFT_MOTOR_FONT, self.LOW)
        wiringpi.pinMode(self.RIGHT_MOTOR_FONT, self.LOW)
        wiringpi.pinMode(self.LEFT_MOTOR_BACK, self.HIGH)
        wiringpi.pinMode(self.RIGHT_MOTOR_BACK, self.HIGH)
        wiringpi.digitalWrite(self.LEFT_MOTOR_BACK, self.HIGH)
        wiringpi.digitalWrite(self.RIGHT_MOTOR_BACK, self.HIGH)
        wiringpi.softPwmWrite(self.LEFT_MOTOR_PWMcontorl, speed1)
        wiringpi.softPwmWrite(self.RIGHT_MOTOR_PWMcontorl, speed2)
        time.sleep(delay)
        self.Motor_stop()

    def SmartCar_turn_Left(self, speed1, speed2, mode, delay):
        '''
        @@@@@@@@
        @@ Developer: Han Cao, id:202244060101
        @@ Fuction name: SmartCar_turn_Left
        @@ Input: 
        @@          Para1-> speed1:(0-100) 
        @@          Para2-> speed2:(0-100)
        @@          Para3-> mode:(1 or 2) 1: left and right motor both in same direction 2: different direction
        @@ Description: Drive 4WDcar turn left , if mode is 1 ,using different speed(speed1>speed2) Make the car turn a corner with a small angle.
            if mode is 2. Make the car turn a corner with a sharp angle
        @@@@@@@@
        '''
        if mode == 1:
            wiringpi.pinMode(self.LEFT_MOTOR_FONT, self.LOW)
            wiringpi.pinMode(self.RIGHT_MOTOR_FONT, self.HIGH)
            wiringpi.pinMode(self.LEFT_MOTOR_BACK, self.HIGH)
            wiringpi.pinMode(self.RIGHT_MOTOR_BACK, self.LOW)
            wiringpi.digitalWrite(self.RIGHT_MOTOR_FONT, self.HIGH)
            wiringpi.digitalWrite(self.LEFT_MOTOR_BACK, self.HIGH)
            wiringpi.softPwmWrite(self.LEFT_MOTOR_PWMcontorl, speed2)
            wiringpi.softPwmWrite(self.RIGHT_MOTOR_PWMcontorl, speed1)
            time.sleep(delay)
        elif mode == 2:
            wiringpi.pinMode(self.LEFT_MOTOR_FONT, self.HIGH)
            wiringpi.pinMode(self.RIGHT_MOTOR_FONT, self.HIGH)
            wiringpi.pinMode(self.LEFT_MOTOR_BACK, self.LOW)
            wiringpi.pinMode(self.RIGHT_MOTOR_BACK, self.LOW)
            wiringpi.digitalWrite(self.RIGHT_MOTOR_FONT, self.HIGH)
            wiringpi.digitalWrite(self.LEFT_MOTOR_BACK, self.HIGH)
            wiringpi.softPwmWrite(self.LEFT_MOTOR_PWMcontorl, speed2)
            wiringpi.softPwmWrite(self.RIGHT_MOTOR_PWMcontorl, speed1)
            time.sleep(delay)
        self.Motor_stop()

    def SmartCar_turn_Right(self, speed1, speed2, mode, delay):
        '''
        @@@@@@@@
        @@ Developer: Han Cao, id:202244060101
        @@ Fuction name: SmartCar_turn_Right
        @@ Input: 
        @@          Para1-> speed1:(0-100) 
        @@          Para2-> speed2:(0-100)
        @@          Para3-> mode:(1 or 2) 1: left and right motor both in same direction 2: different direction
        @@ Description: Drive 4WDcar turn left , if mode is 1 ,using different speed(speed1>speed2) Make the car turn a corner with a small angle.
            if mode is 2. Make the car turn a corner with a sharp angle
        @@@@@@@@
        '''
        if mode == 1:
            wiringpi.pinMode(self.LEFT_MOTOR_FONT, self.HIGH)
            wiringpi.pinMode(self.RIGHT_MOTOR_FONT, self.LOW)
            wiringpi.pinMode(self.LEFT_MOTOR_BACK, self.LOW)
            wiringpi.pinMode(self.RIGHT_MOTOR_BACK, self.HIGH)
            wiringpi.digitalWrite(self.LEFT_MOTOR_FONT, self.HIGH)
            wiringpi.digitalWrite(self.RIGHT_MOTOR_BACK, self.HIGH)
            wiringpi.softPwmWrite(self.LEFT_MOTOR_PWMcontorl, speed1)
            wiringpi.softPwmWrite(self.RIGHT_MOTOR_PWMcontorl, speed2)
            time.sleep(delay)
        elif mode == 2:
            wiringpi.pinMode(self.LEFT_MOTOR_FONT, self.HIGH)
            wiringpi.pinMode(self.RIGHT_MOTOR_FONT, self.HIGH)
            wiringpi.pinMode(self.LEFT_MOTOR_BACK, self.LOW)
            wiringpi.pinMode(self.RIGHT_MOTOR_BACK, self.LOW)
            wiringpi.digitalWrite(self.LEFT_MOTOR_FONT, self.HIGH)
            wiringpi.digitalWrite(self.RIGHT_MOTOR_FONT, self.HIGH)
            wiringpi.softPwmWrite(self.LEFT_MOTOR_PWMcontorl, speed1)
            wiringpi.softPwmWrite(self.RIGHT_MOTOR_PWMcontorl, speed2)
            time.sleep(delay)
        self.Motor_stop()

    # def ServoAngle(self, pos):
    #     # wiringpi.pinMode(self.SERVO_PIN,self.HIGH)
    #     wiringpi.digitalWrite(self.SERVO_PIN,self.HIGH)
    #     wiringpi.softPwmWrite(self.SERVO_PIN, int(2.5 + 10 * pos/180))

    def Motor_stop(self):
        '''
        @@@@@@@@
        @@ Developer: Han Cao, id:202244060101
        @@ Fuction name: Motor_stop
        @@ Input: none 
        @@ Description: stop drive the 4WDcar
        @@@@@@@@
        '''
        wiringpi.digitalWrite(self.LEFT_MOTOR_FONT, self.LOW)
        wiringpi.digitalWrite(self.RIGHT_MOTOR_FONT, self.LOW)
        wiringpi.digitalWrite(self.LEFT_MOTOR_BACK, self.LOW)
        wiringpi.digitalWrite(self.RIGHT_MOTOR_BACK, self.LOW)
        wiringpi.softPwmWrite(self.LEFT_MOTOR_PWMcontorl, 0)
        wiringpi.softPwmWrite(self.RIGHT_MOTOR_PWMcontorl, 0)
        

# if __name__ == '__main__':
#     try:
#         wiringpi.wiringPiSetup()
#         Motor_init()
#         SmartCar_turn_Left(50, 30, 2)
#     except KeyboardInterrupt:
#         Motor_init()
#
