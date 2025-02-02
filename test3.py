from textual.app import App, ComposeResult
from textual.widgets import TextArea


text = '''\
def hello(name):
    print('hello world')

def goodbye(name):
    print(f'{name} good bye')
'''


class TextEditorApp(App):

    def compose(self) -> ComposeResult:
        yield TextArea.code_editor(text,language="java")





# Run the app
if __name__ == "__main__":
    app = TextEditorApp()
    app.run()