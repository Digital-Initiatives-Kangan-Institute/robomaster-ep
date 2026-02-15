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

class WCamera:
    def __init__(self, camera):
        self.camera = camera
        self.RESOLUTION_360P = self.camera.STREAM_360P
    
    def start_stream(self, show_window=True, resolution=None):
        """
        Starts the Robomaster EP video stream using `RESOLUTION_360P`.
        """
        if resolution == None:
            resolution = self.RESOLUTION_360P
        
        self.camera.start_video_stream(display=show_window, resolution=resolution)
    
    def stop_stream(self):
        """
        Stops the Robomaster EP video stream.
        """
        self.camera.stop_video_stream()

class WRobot:
    """
    Wraps the Robomaster EP Robot class
    """
    def __init__(self):
        self.robot = robot.Robot()
        self.chassis = WChassis(self.robot.chassis)
        self.camera = WCamera(self.robot.camera)
    
    def connect(self):
        """
        Initializes and connects to the Robomaster EP in Direct Connect mode.

        You must be connected to the Robomasters Wi-Fi network to connect.
        """
        self.robot.initialize()
    
    def get_chassis(self):
        """
        Gets the Robomaster EP chassis module to perform translations
        """
        return self.chassis
    
    def get_camera(self):
        """
        Gets the Robotmaster camera module.
        """
        return self.camera

    def disconnect(self):
        """
        Disconnects from the Robomaster EP.
        """
        self.robot.close()