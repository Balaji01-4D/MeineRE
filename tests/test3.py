import select
from textual.app import App
from textual.widgets import Select
from textual.reactive import Reactive

class asdm(App[None]):
    options = [('first',Reactive(True)),('second',Reactive(False))]
    def compose(self):
        yield Select(options=self.options,prompt='1 or 2')

    def on_select_changed(self,event: Select.Changed):
        self.notify(f'{event.value}')


def main():
    asdm().run()


if __name__ == '__main__':
    main()
