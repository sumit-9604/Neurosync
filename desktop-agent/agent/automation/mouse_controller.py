import pyautogui


class MouseController:

    @staticmethod
    def move(x: int, y: int):

        pyautogui.moveTo(x, y)

        return {
            "status": "success",
            "x": x,
            "y": y
        }

    @staticmethod
    def click():

        pyautogui.click()

        return {
            "status": "success"
        }

    @staticmethod
    def right_click():

        pyautogui.rightClick()

        return {
            "status": "success"
        }

    @staticmethod
    def double_click():

        pyautogui.doubleClick()

        return {
            "status": "success"
        }

    @staticmethod
    def scroll(amount: int):

        pyautogui.scroll(amount)

        return {
            "status": "success",
            "amount": amount
        }

    @staticmethod
    def get_position():

        x, y = pyautogui.position()

        return {
            "x": x,
            "y": y
        }