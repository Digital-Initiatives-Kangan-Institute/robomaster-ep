"""
WASD Keyboard Control for RoboMaster EP

Controls the robot using WASD keys for movement and Q/E for rotation.
Connects via Access Point mode (robot's Wi-Fi hotspot).

Controls:
    W - Move forward
    S - Move backward
    A - Strafe left
    D - Strafe right
    Q - Rotate left
    E - Rotate right
    ESC - Quit

Usage:
    1. Connect your laptop to the RoboMaster EP's Wi-Fi network
    2. Run this script: python main.py
"""

import sys
import os
import math

# Add the wrapper to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'wrapper'))

import pygame
import cv2

from wrobomaster import WRobot

# Movement settings
MOVE_SPEED = 0.6          # m/s for forward/backward/strafe
ROTATE_SPEED = 60.0       # degrees/s for rotation
CAMERA_FPS = 15           # Display frame rate

# Display settings
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("RoboMaster EP - WASD Control")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 16)

    # Connect to the robot
    print("Connecting to RoboMaster EP (Access Point mode)...")
    print("Make sure you're connected to the robot's Wi-Fi network!")

    ep_robot = WRobot()
    try:
        ep_robot.connect()
    except Exception as e:
        print(f"Failed to connect: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure your laptop is connected to the RoboMaster EP's Wi-Fi")
        print("  2. Check that the robot is powered on")
        print("  3. Try disabling and re-enabling your Wi-Fi")
        pygame.quit()
        sys.exit(1)

    print("Connected!")
    print("Controls: WASD = move, Q/E = rotate, ESC = quit\n")

    chassis = ep_robot.get_chassis()
    camera = ep_robot.get_camera()

    # Start video stream (no built-in window, we'll display in pygame)
    camera.start_stream(show_window=False)

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Get key states for smooth continuous movement
        keys = pygame.key.get_pressed()

        # Calculate movement from WASD
        x_speed = 0.0   # Forward/backward
        y_speed = 0.0   # Left/right strafe
        rotation = 0.0  # Rotation in degrees

        if keys[pygame.K_w]:
            x_speed += MOVE_SPEED
        if keys[pygame.K_s]:
            x_speed -= MOVE_SPEED
        if keys[pygame.K_a]:
            y_speed -= MOVE_SPEED
        if keys[pygame.K_d]:
            y_speed += MOVE_SPEED
        if keys[pygame.K_q]:
            rotation -= ROTATE_SPEED
        if keys[pygame.K_e]:
            rotation += ROTATE_SPEED

        # Send movement command
        # Use duration=0 for indefinite movement until next command
        chassis.translate(x=x_speed, y=y_speed, rotation=rotation, duration=0)

        # Draw display
        screen.fill((30, 30, 30))

        # Get and display camera frame
        try:
            frame = camera.get_cv2_image()
            if frame is not None:
                # Convert BGR to RGB and resize
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                resized = cv2.resize(rgb_frame, (WINDOW_WIDTH, WINDOW_HEIGHT - 60))
                # pygame expects (width, height, 3) but cv2 gives (height, width, 3)
                surface = pygame.surfarray.make_surface(resized.swapaxes(0, 1))
                screen.blit(surface, (0, 0))
        except Exception:
            # Camera might not be ready yet
            pass

        # Draw HUD overlay
        hud_y = WINDOW_HEIGHT - 50

        # Movement indicator
        if x_speed != 0 or y_speed != 0 or rotation != 0:
            direction = []
            if x_speed > 0: direction.append("FWD")
            if x_speed < 0: direction.append("BWD")
            if y_speed > 0: direction.append("RIGHT")
            if y_speed < 0: direction.append("LEFT")
            if rotation > 0: direction.append("ROT-R")
            if rotation < 0: direction.append("ROT-L")
            status_text = "MOVING: " + " + ".join(direction)
            status_color = (0, 255, 0)
        else:
            status_text = "STOPPED"
            status_color = (200, 200, 200)

        # Draw semi-transparent background for HUD
        hud_surface = pygame.Surface((WINDOW_WIDTH, 60))
        hud_surface.set_alpha(180)
        hud_surface.fill((0, 0, 0))
        screen.blit(hud_surface, (0, hud_y))

        # Draw status text
        status = font.render(status_text, True, status_color)
        screen.blit(status, (10, hud_y + 5))

        # Draw controls help
        controls = font.render("WASD=Move  Q/E=Rotate  ESC=Quit", True, (150, 150, 150))
        screen.blit(controls, (10, hud_y + 28))

        pygame.display.flip()
        clock.tick(CAMERA_FPS)

    # Cleanup
    print("\nShutting down...")
    chassis.translate(x=0, y=0, rotation=0, duration=0.1)  # Stop the robot
    camera.stop_stream()
    ep_robot.disconnect()
    pygame.quit()
    print("Done!")


if __name__ == "__main__":
    main()
