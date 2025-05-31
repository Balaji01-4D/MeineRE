from textual.app import App

from meine.screens.help import HelpScreen
from meine.screens.home import HomeScreen
from meine.screens.settings import NameGetterScreen, Settings
from meine.themes import BUILTIN_THEMES
from meine.utils.file_manager import (
    save_history,
    save_settings,
    load_history,
    load_settings,
    initialize_user_data_files
)
initialize_user_data_files()


HOME_SCREEN_ID = "home-screen"
HELP_SCREEN_ID = "help-screen"
SETTINGS_SCREEN_ID = "settings-screen"
CUSTOM_PATH_COMMAND = "Add custom path expansion"
CUSTOM_PATH_HELP = "Add a custom path expansion"


class MeineAI(App[None]):

    def __init__(
        self, driver_class=None, css_path=None, watch_css=False, ansi_color=False
    ):
        super().__init__(driver_class, css_path, watch_css, ansi_color)
        self.more_themes = BUILTIN_THEMES

    async def on_mount(self):
        self.SETTINGS = load_settings()
        self.HISTORY = load_history()
        await self.push_screen(HomeScreen(id=HOME_SCREEN_ID))
        for theme in BUILTIN_THEMES.values():
            self.register_theme(theme)
        self.theme = self.SETTINGS["app_theme"]


    def _on_exit_app(self):
        save_history(self.HISTORY)
        save_settings(self.SETTINGS)
        return super()._on_exit_app()

    def key_ctrl_k(self):
        """
        Handles the Ctrl+K key press event.

        If the current screen is the help screen, it pops the help screen
        from the stack. Otherwise, it pushes the help screen onto the stack.
        """
        if self.screen.id == HELP_SCREEN_ID:
            self.pop_screen()
        elif self.screen.id == SETTINGS_SCREEN_ID:
            self.switch_screen(HelpScreen(id=HELP_SCREEN_ID))
        else:
            self.push_screen(HelpScreen(id=HELP_SCREEN_ID))

    def key_ctrl_s(self):
        """
        Handles the Ctrl+S key press event.

        If the current screen is the settings screen, it pops the settings
        screen from the stack. Otherwise, it pushes the settings screen
        onto the stack.
        """
        if self.screen.id == SETTINGS_SCREEN_ID:
            self.pop_screen()
        elif self.screen.id == HELP_SCREEN_ID:
            self.switch_screen(Settings(id=SETTINGS_SCREEN_ID))
        else:
            self.push_screen(Settings(id=SETTINGS_SCREEN_ID))

    def key_escape(self):
        """
        Handles the Escape key press event.

        If the current screen is not the home screen, it pops the current
        screen from the stack.
        """
        if self.screen.id != HOME_SCREEN_ID:
            self.pop_screen()
        else:
            self.notify("You are in the home screen")


    def push_NameGetter_screen(self, title, callback):
        self.push_screen(NameGetterScreen(title, callback))



app = MeineAI()

def run():
    app.run()



if __name__ == '__main__':
    run()
