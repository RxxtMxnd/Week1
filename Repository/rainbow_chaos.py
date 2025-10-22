import ctypes
import time
import random

# -------------------------
# Setup
# -------------------------
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)
hdc = user32.GetDC(0)

# Rainbow GDI modes (simulate colors)
RAINBOW_MODES = [0x005A0049, 0x008800C6, 0x00CC0020, 0x00440328, 0x00EE0086]

# -------------------------
# DVD-style bouncing bars
# -------------------------
bars = []
for _ in range(5):  # number of bouncing bars
    bar = {
        "x": random.randint(0, width-150),
        "y": random.randint(0, height-80),
        "vx": random.choice([4,5,6]),
        "vy": random.choice([4,5,6]),
        "w": 150,
        "h": 80,
        "mode": random.choice(RAINBOW_MODES),
        "trail": []
    }
    bars.append(bar)

# -------------------------
# Falling rainbow rain
# -------------------------
rain_count = 80
rain = []
for _ in range(rain_count):
    drop = {
        "x": random.randint(0, width-50),
        "y": random.randint(-500, 0),
        "w": 50,
        "h": 50,
        "speed": random.randint(2,6),
        "mode": random.choice(RAINBOW_MODES)
    }
    rain.append(drop)

# -------------------------
# Main Loop
# -------------------------
try:
    while True:
        # -----------------
        # Rainbow rain
        # -----------------
        for drop in rain:
            gdi32.PatBlt(hdc, drop["x"], drop["y"], drop["w"], drop["h"], drop["mode"])
            drop["y"] += drop["speed"]
            if drop["y"] > height:
                drop["y"] = random.randint(-100, 0)
                drop["x"] = random.randint(0, width-50)
                drop["mode"] = random.choice(RAINBOW_MODES)

        # -----------------
        # Bouncing DVD bars
        # -----------------
        for bar in bars:
            # Draw bar
            gdi32.PatBlt(hdc, bar["x"], bar["y"], bar["w"], bar["h"], bar["mode"])

            # Draw trails
            for tx, ty in bar["trail"]:
                gdi32.PatBlt(hdc, tx, ty, bar["w"], bar["h"], random.choice(RAINBOW_MODES))

            # Update trail
            bar["trail"].append((bar["x"], bar["y"]))
            if len(bar["trail"]) > 5:
                bar["trail"].pop(0)

            # Move
            bar["x"] += bar["vx"]
            bar["y"] += bar["vy"]

            bounced = False
            # Bounce + mode change
            if bar["x"] <= 0 or bar["x"] + bar["w"] >= width:
                bar["vx"] = -bar["vx"]
                bounced = True
            if bar["y"] <= 0 or bar["y"] + bar["h"] >= height:
                bar["vy"] = -bar["vy"]
                bounced = True

            if bounced:
                bar["mode"] = random.choice(RAINBOW_MODES)
                # Jelly effect: random offsets
                for _ in range(6):
                    ox = random.randint(-10,10)
                    oy = random.randint(-10,10)
                    gdi32.PatBlt(hdc, max(0,bar["x"]+ox), max(0,bar["y"]+oy), bar["w"], bar["h"], random.choice(RAINBOW_MODES))

        # Small pause for animation speed
        time.sleep(0.01)

except KeyboardInterrupt:
    user32.ReleaseDC(0, hdc)
    print("\nRainbow chaos stopped.")
