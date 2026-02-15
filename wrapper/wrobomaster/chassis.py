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
    
    def unwrap(self):
        """
        Gets the underlying Robomaster EP chassis object (no wrapper).

        Use this when you need to use functionality not exposed by the wrapper.
        """
        return self.chassis