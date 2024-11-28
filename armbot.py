from telemetrix import telemetrix
import math
from time import sleep

class armbot():
    def __init__(
        self,
       
        #  ----------------- geometry of the plotter -----------------
        bounds: tuple = [-8, 4, 6, 13],  # the maximum rectangular drawing area
        inner_arm: float = 8,  # the lengths of the arms
        outer_arm: float = 8,
        #  ----------------- naive calculation values -----------------
        servo_1_parked_pw: int = 1500,  # pulse-widths when parked
        servo_2_parked_pw: int = 1500,
        servo_1_degree_ms: int = -10,  # milliseconds pulse-width per degree
        servo_2_degree_ms: int = 10,  # reversed for the mounting of the shoulder servo
        servo_1_parked_angle: int = -90,  # the arm angle in the parked position
        servo_2_parked_angle: int = 90,
        #  ----------------- hysteresis -----------------
        hysteresis_correction_1: int = 0,  # hardware error compensation
        hysteresis_correction_2: int = 0,
        #  ----------------- the pen -----------------
        pw_up: int = 1500,  # pulse-widths for pen up/down
        pw_down: int = 1100,
        #  ----------------- physical control -----------------
        wait: float = None,  # default wait time between operations
        angular_step: float = None,  # default step of the servos in degrees
        resolution: float = None,  # default resolution of the plotter in cm
    ):

        # set the geometry
        self.inner_arm = inner_arm
        self.outer_arm = outer_arm

        self.inner_pin = 9
        self.outer_pin = 10
        self.pen_pin = 11

        self.wait = 0.5
        
        # Set the x and y position state, so it knows its current x/y position.
        self.x = -self.inner_arm
        self.y = self.outer_arm

        
        self.board = telemetrix.Telemetrix()
        self.board.set_pin_mode_servo(self.inner_pin)
        self.board.set_pin_mode_servo(self.outer_pin)
        self.board.set_pin_mode_servo(self.pen_pin)

      

    def xy_to_angles(self, x=0, y=0):
        """Return the servo angles required to reach any x/y position."""

        hypotenuse = math.sqrt(x**2 + y**2)

        if hypotenuse > self.inner_arm + self.outer_arm:
            raise Exception(
                f"Cannot reach {hypotenuse}; total arm length is {self.inner_arm + self.outer_arm}"
            )

        hypotenuse_angle = math.asin(x / hypotenuse)

        inner_angle = math.acos(
            (hypotenuse**2 + self.inner_arm**2 - self.outer_arm**2)
            / (2 * hypotenuse * self.inner_arm)
        )
        outer_angle = math.acos(
            (self.inner_arm**2 + self.outer_arm**2 - hypotenuse**2)
            / (2 * self.inner_arm * self.outer_arm)
        )

        shoulder_motor_angle = hypotenuse_angle - inner_angle
        elbow_motor_angle = math.pi - outer_angle

        return (90 - math.degrees(shoulder_motor_angle), math.degrees(elbow_motor_angle))
    
    
    def set_angles(self, a,b):
        self.board.servo_write(self.inner_pin,int(a))
        self.board.servo_write(self.outer_pin,int(b))
        sleep(self.wait)

    
    def move(self, x, y):
        angles = self.xy_to_angles(x,y)
        print(f"{x=}")
        print(f"{y=}")
        print(f"{angles=}")
        self.board.servo_write(self.inner_pin,int(angles[0]))
        self.board.servo_write(self.outer_pin,int(angles[1]))
        sleep(self.wait)


    def box(self):
        self.move(1,1)
        self.move(1,4)
        self.move(4,4)
        self.move(4,1)
        self.move(1,1)

    def shutdown(self):
        self.board.servo_detach(self.inner_pin)
        self.board.servo_detach(self.outer_pin)
        self.board.servo_detach(self.pen_pin)
        sleep(0.2)
        self.board.shutdown()
        


if __name__=="__main__":
    arm = armbot()
    arm.box()
    arm.shutdown()

   