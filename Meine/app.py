from functools import partial

from textual.app import App, SystemCommand
from textual.command import Hit, Hits, Provider

from Meine.Actions.system import System
from Meine.exceptions import InfoNotify
from Meine.screens.help import HelpScreen
from Meine.screens.home import HomeScreen
from Meine.screens.settings import NameGetterScreen, Settings
from Meine.themes import BUILTIN_THEMES
from Meine.utils.file_manager import (
    save_history,
    save_settings,
    load_history,
    add_custom_path_expansion,
    load_settings,
    initialize_user_data_files

)
initialize_user_data_files()


HOME_SCREEN_ID = "home-screen"
HELP_SCREEN_ID = "help-screen"
SETTINGS_SCREEN_ID = "settings-screen"
CUSTOM_PATH_COMMAND = "Add custom path expansion"
CUSTOM_PATH_HELP = "Add a custom path expansion"


class CustomCommand(Provider):

    async def search(self, query: str) -> Hits:

        C = "add custom path expansions"
        matcher = self.matcher(query)

        score = matcher.match(C)
        if score > 0:
            yield Hit(
                score,
                matcher.highlight(C),
                partial(
                    self.app.push_screen,
                    NameGetterScreen(title=f"{C}", callback=add_custom_path_expansion),
                ),
                help=f"adding a custom path expansions",
            )


class MeineAI(App[None]):

    COMMANDS = App.COMMANDS | {CustomCommand}

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

    def get_system_commands(self, screen):
        yield from super().get_system_commands(screen)
        yield SystemCommand("Settings", "open settings", self.key_ctrl_s)
        yield SystemCommand("Help", "open the help screen", self.key_ctrl_k)
        yield SystemCommand(
            "shutdown", "shutdown the system after 1 Minute", self.safe_shutdown
        )
        yield SystemCommand(
            "reboot", "reboot the system after 1 Minute", self.safe_reboot
        )

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

    def safe_shutdown(self):
        try:
            sys = System()
            sys.ShutDown()
        except InfoNotify as e:
            if "Minute" in e.message:
                self.notify(e.message)
                self.set_timer(5, self.exit)
            else:
                self.notify(e.message)

    def safe_reboot(self):
        try:
            sys = System()
            sys.Reboot()
        except InfoNotify as e:
            if "Minute" in e.message:
                self.notify(e.message)
                self.set_timer(5, self.exit)
            else:
                self.notify(e.message)

    def push_NameGetter_screen(self, title, callback):
        self.push_screen(NameGetterScreen(title, callback))


def run():
    MeineAI().run()



if __name__ == '__main__':
    run()
