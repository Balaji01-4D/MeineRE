import webbrowser
from pytube import YouTube

from Meine.utils.file_loaders import load_custom_urls
from Meine.exceptions import RaiseNotify


class web:

    def __init__(self):
        self.urls = load_custom_urls()

    def lanuch(self,url: str) -> None:
        if (url in self.urls):
            webbrowser.open(url=url)
            raise RaiseNotify('Opened from the saved urls')
        else :
            webbrowser.open(url=url)


def main():
    w = web()
    webbrowser.open('youtube')

if __name__ == '__main__':
    main()