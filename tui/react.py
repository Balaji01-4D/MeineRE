from textual.widgets import Input,RichLog
from textual.reactive import reactive
from textual.app import App
from rich.panel import Panel
from textual.widget import Widget


class Reat(Widget):

    def compose(self):
        yield RichLog()

    who = reactive(Panel("hello"))
    
    def render(self):
        return f'{self.who}'

class summa(App):


    
    def compose(self):
        yield Input(placeholder='...')
        yield Reat()


    def on_input_changed(self,event:Input.Changed):
        self.query_one(Reat).who = Panel(event.value)
        


summa().run()