import pygame, math

from robomaster import robot, camera, vision

velocity = [0, 0, 0]
line_detected = False
line_centered = False


def on_detect_line_callback(line_info):
    global line_detected, line_centered
    line_type = line_info[0]
    line_detected = line_type == 1
    if line_type == 0:
        return
    line = line_info[1]

    x = line[0]
    y = line[1]
    theta = line[2]
    curve = line[3]

    # Check if the line is close to the center point
    theta_abs = math.fabs(theta)
    line_centered = theta_abs < 5.0

    if x > 0.6:
        velocity[1] += 1
    elif x < 0.4:
        velocity[1] -= 1
    velocity[2] += theta * 8
    print(f"X: {x}, Y: {y}, THETA: {theta} (ABS: {theta_abs}), CURVE: {curve}")


def main():
    global velocity, line_detected, line_centered
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    fill_color = "purple"

    ep_robot = robot.Robot()
    ep_robot.initialize()
    chassis = ep_robot.chassis
    ep_camera = ep_robot.camera
    #ep_vision = ep_robot.vision

    ep_camera.start_video_stream(display=True, resolution=camera.STREAM_360P)
    #vision_result = ep_vision.sub_detect_info(
     #   name="line", color="blue", callback=on_detect_line_callback
    #)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if line_detected and line_centered:
            velocity[0] += 1

        if keys[pygame.K_UP]:
            velocity[0] += 1

        if keys[pygame.K_DOWN]:
            velocity[0] -= 1

        if keys[pygame.K_LEFT]:
            velocity[2] -= 90

        if keys[pygame.K_RIGHT]:
            velocity[2] += 90

        chassis.drive_speed(x=velocity[0], y=velocity[1], z=velocity[2], timeout=0.1)
        velocity = [0, 0, 0]
        screen.fill(fill_color)
        pygame.display.flip()
        clock.tick(60)

    ep_robot.close()
    ep_camera.stop_video_stream()
    pygame.quit()


if __name__ == "__main__":
    main()
