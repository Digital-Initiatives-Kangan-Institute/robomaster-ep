from robomaster import robot

class WChassis:
    def __init__(self, chassis):
        self.chassis = chassis
    
    def translate(self, x: int, y: int, rotation: int, duration: float):
        """
        Translates the Robomaster EP along the x, y and rotation for a duration.
        
        :param x: The amount to move on the x axis.
        :type x: int
        :param y: The amount to move on the y axis.
        :type y: int
        :param rotation: The amount to rotate in degrees.
        :type rotation: int
        :param duration: The duration to translate for.
        :type duration: float
        """
        self.chassis.drive_speed(x, y, rotation, duration)

class WRobot:
    """
    Wraps the Robomaster EP Robot class
    """
    def __init__(self):
        self.robot = robot.Robot()
        self.chassis = WChassis(self.robot.chassis)
    
    def connect(self):
        """
        Initialized and connects to the Robomaster EP in Direct Connect mode.

        You must be connected to the Robomasters Wi-Fi network to connect.
        """
        self.robot.initialize()
    
    def get_chassis(self):
        """
        Gets the Robomaster EP chassis to perform translations
        """
        return self.chassis

    def disconnect(self):
        """
        Disconnects from the Robomaster EP.
        """
        self.robot.close()