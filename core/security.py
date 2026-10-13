from config import (
    ALLOW_SYSTEM_SHUTDOWN,
    ALLOW_RESTART,
    ALLOW_SHELL_COMMANDS
)


DANGEROUS_ACTIONS = {

    "shutdown_pc",

    "restart_pc",

    "shell_command"

}


def is_action_allowed(
    action
):

    if action == "shutdown_pc":

        return ALLOW_SYSTEM_SHUTDOWN

    if action == "restart_pc":

        return ALLOW_RESTART

    if action == "shell_command":

        return ALLOW_SHELL_COMMANDS

    return True


def security_message(action):

    if action == "shutdown_pc":

        return (
            "Shutdown is disabled for safety."
        )

    if action == "restart_pc":

        return (
            "Restart is disabled for safety."
        )

    if action == "shell_command":

        return (
            "Direct shell commands are disabled."
        )

    return (
        f"Action {action} is not allowed."
    )