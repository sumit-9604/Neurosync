import subprocess

class CommandExecutor:

    @staticmethod
    def execute(command: str):

        try:

            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )

            return {
                "status": "success",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }