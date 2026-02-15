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