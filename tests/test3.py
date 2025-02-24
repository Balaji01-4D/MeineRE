import select
from textual.app import App
from textual.widgets import Select, ProgressBar, Footer
from textual.reactive import Reactive
from textual.screen import ModalScreen
from textual.timer import Timer
from textual.containers import Center,Middle

import psutil

class asdm(App[None]):

    def compose(self):
        yield Select([("1",'hello'),("2",'world')])

    def on_select_changed(self,event: Select.Changed):
        self.notify(f'{event.value}')

    def key_ctrl_s(self):
        self.push_screen(Ram())



class Ram(ModalScreen):

    progress_timer: Timer

    def compose(self):

        self.ram_bar = ProgressBar(id='ram-bar',show_eta=False)

        with Center():
            with Middle():
                yield self.ram_bar
        yield Footer()

    def _on_mount(self, event):
        self.progress_timer = self.set_interval(1, self.make_progress, pause=True)

    def make_progress(self):
        ram_usage = psutil.virtual_memory()
        ram_total, ram_used, ram_free = ram_usage.total, ram_usage.used, ram_usage.free
        self.ram_bar.update(total=ram_total,progress=ram_used)

    def key_ctrl_b(self):
        self.progress_timer.resume()

def main():
    asdm().run()


if __name__ == '__main__':


    main()
