import pygame, math, cv2

from wrobomaster import robot, ai

velocity = [0.0, 0.0]
angle = 0.0

line_detected = False
line_centered = False

target_points = None
target_point = None

camera_width = 512
camera_height = 512

STATE_ALIGNING = 0
STATE_DRIVING = 2
STATE_STOPPED = 3

current_state = STATE_STOPPED

def on_detect_line(result: ai.LineTrackerResult):
    #global line_detected, line_centered, velocity, angle, target_point
    global target_point, target_points
    if not result.line_detected or len(result.lines) < 1:
        target_point = None
        target_points = None
    else:
        target_point = result.lines[0]
        target_points = result.lines

def update_state():
    global current_state, target_point

    if target_point == None:
        current_state = STATE_STOPPED
        return
    
    print(f"X: {target_point.x}, Y: {target_point.y}, Theta: {target_point.theta}")
    
    theta_abs = math.fabs(target_point.theta)
    if target_point.x > 0.7 or target_point.x < 0.3 or theta_abs > 10.0:
        current_state = STATE_ALIGNING
        return
    
    current_state = STATE_DRIVING

def execute_state():
    global current_state, target_point, angle, velocity

    if current_state == STATE_STOPPED or target_point == None:
        return
    
    if current_state == STATE_ALIGNING:
        if target_point.x > 0.5:
            velocity[1] += 0.05
        elif target_point.x < 0.5:
            velocity[1] -= 0.05
        angle += target_point.theta
        return
    
    if current_state == STATE_DRIVING:
        velocity[0] += 0.5

def main():
    global velocity, angle, line_detected, line_centered
    pygame.init()
    screen = pygame.display.set_mode((camera_width, camera_height))
    clock = pygame.time.Clock()
    running = True
    fill_color = "purple"

    ep_robot = robot.WRobot()
    ep_robot.connect()
    chassis = ep_robot.get_chassis()
    ep_camera = ep_robot.get_camera()
    ep_vision = ep_robot.unwrap().vision
    ai = ep_robot.get_ai()

    ep_camera.start_stream(show_window=False)
    ai.subscribe_to_line_tracker(on_detect_line, line_color="blue")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Manual
        if keys[pygame.K_UP]:
            velocity[0] += 1.0

        if keys[pygame.K_DOWN]:
            velocity[0] -= 1.0

        if keys[pygame.K_LEFT]:
            angle -= 90

        if keys[pygame.K_RIGHT]:
            angle += 90

        update_state()
        execute_state()

        chassis.translate(x=velocity[0], y=velocity[1], rotation=angle, duration=0.1)

        # Reset velocity and angle (they have been consumed for this tick)
        velocity = [0.0, 0.0]
        angle = 0.0

        screen.fill(fill_color)

        # Draw Start
        frame = ep_camera.get_cv2_image()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resized_frame = cv2.resize(rgb_frame, (camera_width, camera_height))
        surface = pygame.surfarray.make_surface(resized_frame.swapaxes(0, 1))
        screen.blit(surface, (0, 0))

        if target_points != None:
            i = 0
            for line in target_points:
                color = (255, 0, 0)
                if i == 0:
                    color = (0, 255, 0)
                pygame.draw.circle(screen, color, (camera_width * line.x, camera_height * line.y), 10)
                i += 1
        # Draw End

        pygame.display.flip()
        clock.tick(10)

    ep_robot.disconnect()
    ep_camera.stop_stream()
    pygame.quit()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
