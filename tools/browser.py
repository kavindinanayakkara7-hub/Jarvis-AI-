import webbrowser
from urllib.parse import quote_plus


def open_website(url):

    if not url.startswith("http"):

        url = "https://" + url

    webbrowser.open(url)

    return f"Opening {url}."


def search_web(query):

    url = (
        "https://www.google.com/search?q="
        + quote_plus(query)
    )

    webbrowser.open(url)

    return f"Searching Google for {query}."


def search_youtube(query):

    url = (
        "https://www.youtube.com/results?search_query="
        + quote_plus(query)
    )

    webbrowser.open(url)

    return f"Searching YouTube for {query}."