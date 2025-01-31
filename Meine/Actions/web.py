import webbrowser

from Meine.utils.file_loaders import load_custom_urls
from Meine.exceptions import InfoNotify


class web:

    def __init__(self):
        self.urls = load_custom_urls()

    def lanuch(self,url: str) -> None:
        if (url in self.urls):
            webbrowser.open(url=url)
            raise InfoNotify('Opened from the saved urls')
        else :
            webbrowser.open(url=url)


def main():
    w = web()
    webbrowser.open('youtube')

if __name__ == '__main__':
    main()