# open a gcode file and use armbot to draw it


from gcodeparser import GcodeParser
from armbot import armbot

class gcode():

    def __init__(self):
        self.armbot = armbot()

    def draw(self, filename):
        with open(filename, 'r') as f:
            gcode = f.read()
            for line in GcodeParser(gcode).lines:
                print(line)
                if line.command == ('G', 1):
                    self.armbot.move(line.params["X"],line.params["Y"])
        self.armbot.shutdown()


        

if __name__=="__main__":
    gcode = gcode()
    gcode.draw('hello100.gcode')

