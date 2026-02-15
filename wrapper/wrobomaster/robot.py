from robomaster import robot

from camera import WCamera
from chassis import WChassis
from ai import WAI

class WRobot:
    """
    Wraps the Robomaster EP Robot class
    """
    def __init__(self):
        self.robot = robot.Robot()
        self.chassis = WChassis(self.robot.chassis)
        self.camera = WCamera(self.robot.camera)
        self.ai = WAI(self.robot)
    
    def connect(self):
        """
        Connects to the Robomaster EP using Direct Connect mode.

        You must be connected to the Robomaster EP Wi-Fi network.
        """
        self.robot.initialize()
    
    def get_chassis(self):
        """
        Gets the Robomaster EP chassis module to perform translations
        """
        return self.chassis
    
    def get_camera(self):
        """
        Gets the Robomaster EP camera module.
        """
        return self.camera

    def get_ai(self):
        """
        Gets the Robomaster EP ai module.

        This module contains vision related AI functions.
        """
        return self.ai

    def disconnect(self):
        """
        Disconnects from the Robomaster EP.
        """
        self.robot.close()
    
    def unwrap(self):
        """
        Gets the underlying Robomaster EP robot object (no wrapper).

        Use this when you need to use functionality not exposed by the wrapper.
        """
        return self.robot