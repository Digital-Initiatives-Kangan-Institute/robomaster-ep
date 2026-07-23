"""
Camera Viewer for RoboMaster EP

Displays the live camera feed from the robot.
Useful for checking camera feed and verifying connection.

Usage:
    1. Connect your laptop to the RoboMaster EP's Wi-Fi network
    2. Run this script: python main.py
    3. Press ESC or close the window to quit
"""

import sys
import os

# Add the wrapper to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'wrapper'))

import pygame
import cv2

from wrobomaster import WRobot

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 30


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("RoboMaster EP - Camera Viewer")
    clock = pygame.time.Clock()

    print("Connecting to RoboMaster EP...")
    print("Make sure you're connected to the robot's Wi-Fi network!")

    ep_robot = WRobot()
    try:
        ep_robot.connect()
    except Exception as e:
        print(f"Failed to connect: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure your laptop is connected to the RoboMaster EP's Wi-Fi")
        print("  2. Check that the robot is powered on")
        pygame.quit()
        sys.exit(1)

    print("Connected! Press ESC or close window to quit.\n")

    camera = ep_robot.get_camera()
    camera.start_stream(show_window=False)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill((30, 30, 30))

        try:
            frame = camera.get_cv2_image()
            if frame is not None:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                resized = cv2.resize(rgb_frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
                surface = pygame.surfarray.make_surface(resized.swapaxes(0, 1))
                screen.blit(surface, (0, 0))
        except Exception:
            pass

        pygame.display.flip()
        clock.tick(FPS)

    print("Shutting down...")
    camera.stop_stream()
    ep_robot.disconnect()
    pygame.quit()
    print("Done!")


if __name__ == "__main__":
    main()
