from textual.app import App
from Meine.logger_config import logger

class someapp(App[None]):

    def on_click(self,event):
        logger.info(f'{event.widget.id}')



someapp().run()