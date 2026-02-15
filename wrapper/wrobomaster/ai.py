from typing import Callable

class LineTrackerItem:
    def __init__(self, x: int, y: int, theta: float, curvature: float):
        self.x = x
        self.y = y
        self.theta = theta
        self.curvature = curvature

class LineTrackerResult:
    def __init__(self):
        self.line_detected: bool = False
        self.lines: list[LineTrackerItem] = []

class WAI:
    def __init__(self, robot):
        self.robot = robot
        self.vision = robot.vision
        self.line_tracker_callback = None
    
    def _line_tracker_callback(self, line_info):
        if self.line_tracker_callback == None:
            return
        
        result = LineTrackerResult()

        line_type = line_info[0]
        result.line_detected = line_type != 0

        if result.line_detected:
            for i in range(1, len(line_info)):
                line = line_info[i]
                x = line[0]
                y = line[1]
                theta = line[2]
                curve = line[3]
                result.lines.append(LineTrackerItem(x, y, theta, curve))
        
        self.line_tracker_callback(result)

    def subscribe_to_line_tracker(self, callback: Callable[[LineTrackerResult], None], line_color="blue"):
        self.line_tracker_callback = callback
        self.vision.sub_detect_info(
            name="line", color=line_color, callback=self._line_tracker_callback
        )