import webbrowser

from Meine.exceptions import InfoNotify
from Meine.utils.file_loaders import load_custom_urls


class web:

    def __init__(self):
        self.urls = load_custom_urls()

    def lanuch(self, url: str) -> None:
        if url in self.urls:
            webbrowser.open(url=url)
            raise InfoNotify("Opened from the saved urls")
        else:
            webbrowser.open(url=url)
