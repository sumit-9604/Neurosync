import pyautogui


class KeyboardController:

    @staticmethod
    def type_text(text: str):

        pyautogui.write(text)

        return {
            "status": "success"
        }

    @staticmethod
    def press_key(key: str):

        pyautogui.press(key)

        return {
            "status": "success",
            "key": key
        }

    @staticmethod
    def hotkey(*keys):

        pyautogui.hotkey(*keys)

        return {
            "status": "success",
            "keys": list(keys)
        }

    @staticmethod
    def copy():

        pyautogui.hotkey("ctrl", "c")

        return {
            "status": "success"
        }

    @staticmethod
    def paste():

        pyautogui.hotkey("ctrl", "v")

        return {
            "status": "success"
        }

    @staticmethod
    def select_all():

        pyautogui.hotkey("ctrl", "a")

        return {
            "status": "success"
        }