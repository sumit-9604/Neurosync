from automation.app_launcher import AppLauncher
from automation.mouse_controller import MouseController
from automation.keyboard_controller import KeyboardController


def execute(command: dict):

    action = command.get("action")

    if action == "open_chrome":
        return AppLauncher.open_chrome()

    elif action == "open_vscode":
        return AppLauncher.open_vscode()

    elif action == "mouse_move":
        return MouseController.move(
            command["x"],
            command["y"]
        )

    elif action == "mouse_click":
        return MouseController.click()

    elif action == "type_text":
        return KeyboardController.type_text(
            command["text"]
        )

    else:
        return {
            "status": "error",
            "message": "Unknown command"
        }