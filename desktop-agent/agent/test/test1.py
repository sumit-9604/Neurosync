# TEST FOR THE APPLAUNCHER , MOUSE CONTROLLER , KEYBOARD CONTROLLER

from agent.automation.app_launcher import AppLauncher
from agent.automation.keyboard_controller import KeyboardController
from agent.automation.mouse_controller import MouseController
import time
print("Opening Notepad...")

AppLauncher.open_notepad()

time.sleep(2)

print("Typing...")

KeyboardController.type_text(
    "Hello from NeuroLink!"
)

time.sleep(1)

print("Moving mouse...")

MouseController.move(500,500)

time.sleep(1)

MouseController.click()

print("Done!")