import ctypes
import time

# Load required functions
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

# Constants
PATINVERT = 0x005A0049  # Inverts pixels (glitch effect)

# Get screen dimensions
width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)

# Get desktop device context
hdc = user32.GetDC(0)

# Rectangle size
rect_w = 150
rect_h = 80

# Starting position & velocity
x = 100
y = 100
vx = 5  # Horizontal speed
vy = 5  # Vertical speed

try:
    while True:
        # Draw the rectangle (invert pixels at this location)
        gdi32.PatBlt(hdc, x, y, rect_w, rect_h, PATINVERT)

        # Pause briefly
        time.sleep(0.01)

        # Erase it by inverting again (so it looks smooth)
        gdi32.PatBlt(hdc, x, y, rect_w, rect_h, PATINVERT)

        # Move
        x += vx
        y += vy

        # Bounce off edges
        if x <= 0 or x + rect_w >= width:
            vx = -vx
        if y <= 0 or y + rect_h >= height:
            vy = -vy

except KeyboardInterrupt:
    # Cleanup if stopped
    user32.ReleaseDC(0, hdc)
