import Motor

motor = Motor.MotorControl()
motor.Motor_init()

try:
    motor.SmartCar_turn_Left(50,50,0.1)
except KeyboardInterrupt:
    motor.Motor_stop()
    motor.Motor_init()

