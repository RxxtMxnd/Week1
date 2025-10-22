import ctypes
import time
import random

# Load required functions
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

# Constants
PATINVERT = 0x005A0049  # Inverts pixels

# Get screen dimensions
width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)

# Get desktop device context
hdc = user32.GetDC(0)

# Rectangle settings
rect_height = 40  # Height of each falling bar
rect_speed = 8    # Speed in pixels

# Generate multiple random X positions for rectangles
rectangles = [random.randint(0, width) for _ in range(10)]  # 10 falling bars

# Animate
for y in range(0, height, rect_speed):
    for x in rectangles:
        gdi32.PatBlt(hdc, x, y, 80, rect_height, PATINVERT)  # 80px wide
    time.sleep(0.01)

# Release DC
user32.ReleaseDC(0, hdc)
