import ctypes
import time

# Load required functions
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

# Constants
PATINVERT = 0x005A0049  # Inverts pixels
SRCCOPY = 0x00CC0020

# Get screen dimensions
width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)

# Get desktop device context
hdc = user32.GetDC(0)

# Rectangle settings
rect_height = 50  # Thickness of the bar
speed = 5         # Pixels per frame

# Slide down the screen
for y in range(0, height, speed):
    gdi32.PatBlt(hdc, 0, y, width, rect_height, PATINVERT)
    time.sleep(0.01)

# Release DC
user32.ReleaseDC(0, hdc)
