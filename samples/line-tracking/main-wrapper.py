import pygame, math

from wrobomaster import robot, ai

velocity = [0.0, 0.0]
angle = 0.0

line_detected = False
line_centered = False

current_line_result = None


def on_detect_line(result: ai.LineTrackerResult):
    global line_detected, line_centered, velocity, angle, current_line_result
    current_line_result = result

    line_detected = result.line_detected
    print(f"Line Detected: {line_detected}")

    if not result.line_detected:
        return
    
    line = result.lines[0]
    
    # Check if the line is close to the center point
    theta_abs = math.fabs(line.theta)
    line_centered = theta_abs < 10.0

    if line.x > 0.6:
        velocity[1] += 0.05
    elif line.x < 0.4:
        velocity[1] -= 0.05

    if not line_centered:
        angle += line.theta

    print(f"X: {line.x}, Y: {line.y}, THETA: {line.theta} (ABS: {theta_abs}), CURVE: {line.curvature}, CENTER: {line_centered}")
    print(line.theta)


def main():
    global velocity, angle, line_detected, line_centered
    pygame.init()
    screen = pygame.display.set_mode((256, 256))
    clock = pygame.time.Clock()
    running = True
    fill_color = "purple"

    ep_robot = robot.WRobot()
    ep_robot.connect()
    chassis = ep_robot.get_chassis()
    ep_camera = ep_robot.get_camera()
    ep_vision = ep_robot.unwrap().vision
    ai = ep_robot.get_ai()

    ep_camera.start_stream()
    ai.subscribe_to_line_tracker(on_detect_line, line_color="blue")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Automated (Line Tracker)
        if line_detected and line_centered:
            velocity[0] += 0.5

        # Manual
        if keys[pygame.K_UP]:
            velocity[0] += 1.0

        if keys[pygame.K_DOWN]:
            velocity[0] -= 1.0

        if keys[pygame.K_LEFT]:
            angle -= 90

        if keys[pygame.K_RIGHT]:
            angle += 90

        chassis.translate(x=velocity[0], y=velocity[1], rotation=angle, duration=0.1)

        # Reset velocity and angle (they have been consumed for this tick)
        velocity = [0.0, 0.0]
        angle = 0.0

        screen.fill(fill_color)
        pygame.display.flip()
        clock.tick(10)

    ep_robot.disconnect()
    ep_camera.stop_stream()
    pygame.quit()


if __name__ == "__main__":
    main()
