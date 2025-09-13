"""
Displays live mouse coordinates until Ctrl-C is pressed.
Run, hover over a UI element, press Ctrl-C, copy the number shown.
"""
import pyautogui, time

print("Move mouse; press Ctrl-C to grab current position.")
try:
    while True:
        x, y = pyautogui.position()
        print(f"\r({x:4d}, {y:4d})", end="", flush=True)
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\nCoordinate captured.")
