class WCamera:
    def __init__(self, camera):
        self.camera = camera
        
        self.STREAM_360P = "360p"
        self.STREAM_540P = "540p"
        self.STREAM_720P = "720p"
    
    def start_stream(self, show_window=True, resolution="360p"):
        """
        Starts the Robomaster EP video stream.
        
        :param show_window: 
            When `true`, shows a window with the stream (`true` by default).

        :param resolution: There are three supported resolutions

            - `360p`
            - `540p`
            - `720p`

            If no resolution is provided, `360p` is enabled by default.
        """
        
        self.camera.start_video_stream(display=show_window, resolution=resolution)
    
    def stop_stream(self):
        """
        Stops the Robomaster EP video stream.
        """
        self.camera.stop_video_stream()
    
    def unwrap(self):
        """
        Gets the underlying Robomaster EP camera object (no wrapper).

        Use this when you need to use functionality not exposed by the wrapper.
        """
        return self.camera