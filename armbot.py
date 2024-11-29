# Inspired heavily by brachiograph https://www.brachiograph.art/
# Main class to drive the arm


from telemetrix import telemetrix
import math
from time import sleep

class armbot():
    def __init__(
        self,
        #  ----------------- geometry of the plotter -----------------
        # the maximum rectangular drawing area in milimeters :
        xmin: float = -10,
        ymin: float = 10,
        xmax: float = 110,
        ymax: float = 110,
        inner_arm_length: float = 80,  # the lengths of the arms in milimeters
        outer_arm_length: float = 80,
        feedrate: int = 1200, # default feedrate of the machine in milimeter per minute = 10 mm per second
        resolution: float = 1, # distance in mm between each move
        #  ----------------- servo pins -----------------
        inner_servo_pin: int = 9,
        outer_servo_pin: int = 10,
        pen_servo_pin: int = 11,

       
    ):

        # set the geometry
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.inner_arm_length = inner_arm_length
        self.outer_arm_length = outer_arm_length
        self.feedrate = feedrate
        self.resolution = resolution

        # set the servo pins
        self.inner_servo_pin = inner_servo_pin
        self.outer_servo_pin = outer_servo_pin
        self.pen_servo_pin = pen_servo_pin

        self.wait = 0.5

        self.startup()

        # we assume the bot is parked already :
        self.x = self.xmin
        self.y = self.ymin
        
        
    def startup(self):    
        self.board = telemetrix.Telemetrix()
        self.board.set_pin_mode_servo(self.inner_servo_pin)
        self.board.set_pin_mode_servo(self.outer_servo_pin)
        self.board.set_pin_mode_servo(self.pen_servo_pin)

    def shutdown(self):
        self.park()
        self.board.servo_detach(self.inner_servo_pin)
        self.board.servo_detach(self.outer_servo_pin)
        self.board.servo_detach(self.pen_servo_pin)
        sleep(0.2)
        self.board.shutdown()
      
    # this is copied straight from brachiograph : 
    def xy_to_angles(self, x=0, y=0):
        """Return the servo angles required to reach any x/y position."""

        hypotenuse = math.sqrt(x**2 + y**2)

        if hypotenuse > self.inner_arm_length + self.outer_arm_length:
            print(f"Cannot reach {hypotenuse}; total arm length is {self.inner_arm_length + self.outer_arm_length}")
            #raise Exception(
            #    f"Cannot reach {hypotenuse}; total arm length is {self.inner_arm_length + self.outer_arm_length}"
            #)

        hypotenuse_angle = math.asin(x / hypotenuse)

        inner_angle = math.acos(
            (hypotenuse**2 + self.inner_arm_length**2 - self.outer_arm_length**2)
            / (2 * hypotenuse * self.inner_arm_length)
        )
        outer_angle = math.acos(
            (self.inner_arm_length**2 + self.outer_arm_length**2 - hypotenuse**2)
            / (2 * self.inner_arm_length * self.outer_arm_length)
        )

        shoulder_motor_angle = hypotenuse_angle - inner_angle
        elbow_motor_angle = math.pi - outer_angle

        return (math.degrees(shoulder_motor_angle), math.degrees(elbow_motor_angle))
    
    
    def set_angles(self, a,b):
        self.board.servo_write(self.inner_servo_pin, 90 - int(a))
        self.board.servo_write(self.outer_servo_pin, int(b))
        

    
    def move(self, x, y):
        # handle the fact that xmin and ymin is in fact our 0
        x = x + self.xmin
        y = y + self.ymin

        # enforce limits
        if (x < self.xmin): 
            x = self.xmin
            print('xmin reached')
        if (x > self.xmax): 
            x = self.xmax
            print('xmax reached')
        if (y < self.ymin): 
            y = self.ymin
            print('ymin reached')
        if (y > self.ymax): 
            y = self.ymax
            print('ymax reached')

        # calculate distance in order to set steps and speed
        distance = ((x - self.x) ** 2 + (y - self.y) ** 2) ** 0.5

        print(f"{self.x=}")
        print(f"{self.y=}")
        print(f"{distance=} mm")

        if (distance > 0.001):        
            no_of_steps = round(distance / self.resolution) or 1
            (x_distance, y_distance) = (x - self.x, y - self.y)
            (x_distance_per_step, y_distance_per_step) = (x_distance / no_of_steps, y_distance / no_of_steps)
            step_time = distance / self.feedrate * 60 / no_of_steps 
            print(f"{step_time=} seconds")
            

            for step in range(no_of_steps):
                # update current position
                self.x = self.x + x_distance_per_step
                self.y = self.y + y_distance_per_step
                # calculates angles
                angle_1, angle_2 = self.xy_to_angles(self.x, self.y)
                self.set_angles(angle_1, angle_2)

                sleep(step_time)

                #print(f"{self.x=}")
                #print(f"{self.y=}")
        


    def pen_up(self):
        self.board.servo_write(self.pen_servo_pin, 0)
        
    def pen_down(self):
        self.board.servo_write(self.pen_servo_pin, 180)
        
    


    def box(self):
        self.move(self.xmin,self.ymin)
        self.move(self.xmin,self.ymax)
        self.move(self.xmax,self.ymax)
        self.move(self.xmax,self.ymin)
        self.move(self.xmin,self.ymin)

    

    def park(self):
        self.move(0, 0)
        


if __name__=="__main__":
    arm = armbot()
    arm.box()
    arm.park()
    arm.shutdown()

   