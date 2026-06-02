import subprocess
import platform
import os


class AppLauncher:

    @staticmethod
    def open_chrome():
        try:
            if platform.system() == "Windows":
                subprocess.Popen("start chrome", shell=True)
            elif platform.system() == "Linux":
                subprocess.Popen(["google-chrome"])
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", "-a", "Google Chrome"])

            return {"status": "success"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def open_vscode():
        try:
            subprocess.Popen("code", shell=True)

            return {"status": "success"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def open_notepad():
        try:
            if platform.system() == "Windows":
                subprocess.Popen("notepad")

            return {"status": "success"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def open_terminal():
        try:
            if platform.system() == "Windows":
                subprocess.Popen("cmd")

            return {"status": "success"}

        except Exception as e:
            return {"status": "error", "message": str(e)}