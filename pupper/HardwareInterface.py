import pigpio
from pca9685_driver import Device
from pupper.Config import ServoParams, PWMParams

class HardwareInterface:
    def __init__(self):
        self.pca9685 = Device(0x40)
        self.pwm_params = PWMParams()
        self.servo_params = ServoParams()
        initialize_pwm(self.pca9685, self.pwm_params)

    def set_actuator_postions(self, joint_angles):
        send_servo_commands(self.pca9685, self.pwm_params, self.servo_params, joint_angles)
    
    def set_actuator_position(self, joint_angle, axis, leg):
        send_servo_command(self.pca9685, self.pwm_params, self.servo_params, joint_angle, axis, leg)


def pwm_to_duty_cycle(pulsewidth_micros, pwm_params):
    """Converts a pwm signal (measured in microseconds) to a corresponding duty cycle on the gpio pwm pin

    Parameters
    ----------
    pulsewidth_micros : float
        Width of the pwm signal in microseconds
    pwm_params : PWMParams
        PWMParams object

    Returns
    -------
    float
        PWM duty cycle corresponding to the pulse width
    """
    return int(pulsewidth_micros / 1e6 * pwm_params.freq * pwm_params.resolution)


def angle_to_pwm(angle, servo_params, axis_index, leg_index):
    """Converts a desired servo angle into the corresponding PWM command

    Parameters
    ----------
    angle : float
        Desired servo angle, relative to the vertical (z) axis
    servo_params : ServoParams
        ServoParams object
    axis_index : int
        Specifies which joint of leg to control. 0 is abduction servo, 1 is inner hip servo, 2 is outer hip servo.
    leg_index : int
        Specifies which leg to control. 0 is front-right, 1 is front-left, 2 is back-right, 3 is back-left.

    Returns
    -------
    float
        PWM width in microseconds
    """
    angle_deviation = (
        angle - servo_params.neutral_angles[axis_index, leg_index]
    ) * servo_params.servo_multipliers[axis_index, leg_index]
    pulse_width_micros = (
        servo_params.neutral_position_pwm
        + servo_params.micros_per_rad * angle_deviation
    )
    return pulse_width_micros


def angle_to_duty_cycle(angle, pwm_params, servo_params, axis_index, leg_index):
    return pwm_to_duty_cycle(
        angle_to_pwm(angle, servo_params, axis_index, leg_index), pwm_params
    )


def initialize_pwm(dev, pwm_params):
    #TODO: enable with OE pin
    dev.set_pwm_frequency(pwm_params.freq)


def send_servo_commands(dev, pwm_params, servo_params, joint_angles):
    for leg_index in range(4):
        for axis_index in range(3):
            duty_cycle = angle_to_duty_cycle(
                joint_angles[axis_index, leg_index],
                pwm_params,
                servo_params,
                axis_index,
                leg_index,
            )
            dev.set_pwm(pwm_params.channels[axis_index, leg_index], duty_cycle)


def send_servo_command(dev, pwm_params, servo_params, joint_angle, axis, leg):
    duty_cycle = angle_to_duty_cycle(joint_angle, pwm_params, servo_params, axis, leg)
    dev.set_pwm(pwm_params.channels[axis, leg], duty_cycle)


def deactivate_servos(dev, pwm_params):
    #TODO: disable with OE pin
    for leg_index in range(4):
        for axis_index in range(3):
            dev.set_pwm(pwm_params.channels[axis_index, leg_index], 0)
