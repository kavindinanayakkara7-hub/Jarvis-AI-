import os
import glob


def create_folder(path):

    try:

        os.makedirs(
            os.path.expanduser(path),
            exist_ok=True
        )

        return f"Folder created: {path}"

    except Exception as error:

        return f"Could not create folder: {error}"


def create_file(path, content=""):

    try:

        path = os.path.expanduser(path)

        parent = os.path.dirname(path)

        if parent:
            os.makedirs(
                parent,
                exist_ok=True
            )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(content)

        return f"File created: {path}"

    except Exception as error:

        return f"Could not create file: {error}"


def find_files(directory, pattern="*"):

    try:

        directory = os.path.expanduser(
            directory
        )

        search_path = os.path.join(
            directory,
            "**",
            pattern
        )

        results = glob.glob(
            search_path,
            recursive=True
        )

        results = results[:50]

        if not results:

            return "No files found."

        output = "\n".join(
            results
        )

        return (
            f"Found {len(results)} files:\n"
            + output
        )

    except Exception as error:

        return f"File search failed: {error}"