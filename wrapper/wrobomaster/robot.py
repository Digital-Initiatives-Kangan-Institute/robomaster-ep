from robomaster import robot

from wrobomaster.camera import WCamera
from wrobomaster.chassis import WChassis
from wrobomaster.ai import WAI

class WRobot:
    """
    Wraps the Robomaster EP Robot class
    """
    def __init__(self):
        self.robot = robot.Robot()
        self.chassis = None
        self.camera = None
        self.ai = None
    
    def connect(self):
        """
        Connects to the Robomaster EP using Direct Connect mode.

        You must be connected to the Robomaster EP Wi-Fi network.
        """
        self.robot.initialize()
        self.chassis = WChassis(self.robot.chassis)
        self.camera = WCamera(self.robot.camera)
        self.ai = WAI(self.robot)
    
    def get_chassis(self):
        """
        Gets the Robomaster EP chassis module to perform translations
        """
        if not self.robot.is_initialized or self.chassis == None:
            raise Exception("You must connect to the Robomaster before getting modules.")
        
        return self.chassis
    
    def get_camera(self):
        """
        Gets the Robomaster EP camera module.
        """
        if not self.robot.is_initialized or self.camera == None:
            raise Exception("You must connect to the Robomaster before getting modules.")
        
        return self.camera

    def get_ai(self):
        """
        Gets the Robomaster EP ai module.

        This module contains vision related AI functions.
        """
        if not self.robot.is_initialized or self.ai == None:
            raise Exception("You must connect to the Robomaster before getting modules.")
        
        return self.ai

    def disconnect(self):
        """
        Disconnects from the Robomaster EP.
        """
        self.robot.close()
        self.chassis = None
        self.camera = None
        self.ai = None
    
    def unwrap(self):
        """
        Gets the underlying Robomaster EP robot object (no wrapper).

        Use this when you need to use functionality not exposed by the wrapper.
        """
        return self.robot