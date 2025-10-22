import ctypes
import time
import random


user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)
hdc = user32.GetDC(0)


MODES = [0x005A0049, 0x008800C6, 0x00CC0020, 0x00440328]  # PATINVERT, SRCERASE, SRCCOPY, SRCAND


rect_w = 150
rect_h = 80


x = random.randint(0, width - rect_w)
y = random.randint(0, height - rect_h)
vx = random.choice([4, 5, 6])
vy = random.choice([4, 5, 6])

mode_index = 0


trail = []


jelly_strength = 8

# -------------------------
# Main loop
# -------------------------
try:
    while True:
        # Draw rectangle
        gdi32.PatBlt(hdc, x, y, rect_w, rect_h, MODES[mode_index])

        # Draw trails
        for tx, ty in trail:
            gdi32.PatBlt(hdc, tx, ty, rect_w, rect_h, MODES[(mode_index+1)%len(MODES)])

        time.sleep(0.01)

        # Erase rectangle
        gdi32.PatBlt(hdc, x, y, rect_w, rect_h, MODES[mode_index])
        # Erase oldest trail
        if trail:
            tx, ty = trail.pop(0)
            gdi32.PatBlt(hdc, tx, ty, rect_w, rect_h, MODES[(mode_index+1)%len(MODES)])

        
        trail.append((x, y))
        if len(trail) > 5:  # trail length
            trail.pop(0)

        
        x += vx
        y += vy

        bounced = False

        
        if x <= 0 or x + rect_w >= width:
            vx = -vx + random.choice([-1,1])  # slight speed change
            bounced = True
        if y <= 0 or y + rect_h >= height:
            vy = -vy + random.choice([-1,1])
            bounced = True

        # Corner impact
        if bounced:
            mode_index = (mode_index + 1) % len(MODES)
            # Jelly distortion: random offsets around rectangle
            for _ in range(jelly_strength):
                ox = random.randint(-10,10)
                oy = random.randint(-10,10)
                gdi32.PatBlt(hdc, max(0,x+ox), max(0,y+oy), rect_w, rect_h, MODES[mode_index])

except KeyboardInterrupt:
    user32.ReleaseDC(0, hdc)
    print("\nGlitch storm stopped.")

