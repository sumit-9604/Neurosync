# TESTING FOR THE COMMAND EXECUTER

from agent.terminal.command_executor import CommandExecutor

result = CommandExecutor.execute(
    "python --version"
)

print(result)