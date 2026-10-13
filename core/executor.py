from tools.apps import (
    open_app,
    close_app
)

from tools.browser import (
    open_website,
    search_web,
    search_youtube
)

from tools.files import (
    create_folder,
    create_file,
    find_files
)

from tools.system import (
    get_system_info,
    get_current_time,
    get_current_date
)

from tools.keyboard import (
    type_text,
    press_key,
    hotkey,
    click
)

from tools.screenshot import (
    take_screenshot
)

from ai.memory import (
    remember,
    get_memories,
    clear_memory
)

from core.security import (
    is_action_allowed,
    security_message
)


def execute_action(
    action,
    parameters=None
):

    parameters = parameters or {}

    if not is_action_allowed(action):

        return security_message(
            action
        )

    try:

        # =================================================
        # APPLICATIONS
        # =================================================

        if action == "open_app":

            return open_app(
                parameters.get(
                    "app",
                    ""
                )
            )

        if action == "close_app":

            return close_app(
                parameters.get(
                    "app",
                    ""
                )
            )

        # =================================================
        # BROWSER
        # =================================================

        if action == "open_website":

            return open_website(
                parameters.get(
                    "url",
                    ""
                )
            )

        if action == "search_web":

            return search_web(
                parameters.get(
                    "query",
                    ""
                )
            )

        if action == "search_youtube":

            return search_youtube(
                parameters.get(
                    "query",
                    ""
                )
            )

        # =================================================
        # FILES
        # =================================================

        if action == "create_folder":

            return create_folder(
                parameters.get(
                    "path",
                    ""
                )
            )

        if action == "create_file":

            return create_file(
                parameters.get(
                    "path",
                    ""
                ),
                parameters.get(
                    "content",
                    ""
                )
            )

        if action == "find_files":

            return find_files(
                parameters.get(
                    "directory",
                    "."
                ),
                parameters.get(
                    "pattern",
                    "*"
                )
            )

        # =================================================
        # SYSTEM
        # =================================================

        if action == "get_system_info":

            return get_system_info()

        if action == "get_current_time":

            return get_current_time()

        if action == "get_current_date":

            return get_current_date()

        # =================================================
        # KEYBOARD
        # =================================================

        if action == "type_text":

            return type_text(
                parameters.get(
                    "text",
                    ""
                )
            )

        if action == "press_key":

            return press_key(
                parameters.get(
                    "key",
                    ""
                )
            )

        if action == "hotkey":

            keys = parameters.get(
                "keys",
                []
            )

            return hotkey(
                *keys
            )

        if action == "click":

            return click(
                parameters.get(
                    "x",
                    0
                ),
                parameters.get(
                    "y",
                    0
                )
            )

        # =================================================
        # SCREENSHOT
        # =================================================

        if action == "take_screenshot":

            return take_screenshot()

        # =================================================
        # MEMORY
        # =================================================

        if action == "remember":

            return remember(
                parameters.get(
                    "text",
                    ""
                )
            )

        if action == "get_memory":

            memories = get_memories()

            if not memories:

                return "I don't have any saved memories."

            return (
                "I remember:\n"
                + "\n".join(
                    f"- {item}"
                    for item in memories
                )
            )

        if action == "clear_memory":

            return clear_memory()

        # =================================================
        # UNKNOWN
        # =================================================

        return (
            f"I don't know how to perform "
            f"the action: {action}"
        )

    except Exception as error:

        return (
            f"Action failed: {error}"
        )


def execute_plan(plan):

    if not plan:

        return "I don't have a plan."

    plan_type = plan.get(
        "type"
    )

    # =====================================================
    # CHAT
    # =====================================================

    if plan_type == "chat":

        return plan.get(
            "message",
            "I don't have a response."
        )

    # =====================================================
    # SINGLE ACTION
    # =====================================================

    if plan_type == "action":

        action = plan.get(
            "action"
        )

        parameters = plan.get(
            "parameters",
            {}
        )

        return execute_action(
            action,
            parameters
        )

    # =====================================================
    # MULTI ACTION
    # =====================================================

    if plan_type == "multi_action":

        actions = plan.get(
            "actions",
            []
        )

        results = []

        for item in actions:

            action = item.get(
                "action"
            )

            parameters = item.get(
                "parameters",
                {}
            )

            result = execute_action(
                action,
                parameters
            )

            results.append(
                result
            )

        return "\n".join(
            results
        )

    return (
        "I could not understand the AI plan."
    )