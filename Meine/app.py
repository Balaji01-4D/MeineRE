from functools import partial
from pathlib import Path

from textual.app import App, SystemCommand
from textual.command import Hit, Hits, Provider

from Meine.Actions.system import System
from Meine.exceptions import InfoNotify
from Meine.logger_config import logger
from Meine.Screens.help import HelpScreen
from Meine.Screens.home import HomeScreen
from Meine.Screens.settings import NameGetterScreen, Settings
from Meine.utils.file_editor import add_custom_path_expansion
from Meine.utils.file_loaders import load_settings

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

    SETTINGS = load_settings()

    COMMANDS = App.COMMANDS | {CustomCommand}

    async def on_mount(self):
        await self.push_screen(HomeScreen(id=HOME_SCREEN_ID))
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

    def key_ctrl_k(self):
        try:
            if self.screen_stack[-1] == "help_screen":
                self.pop_screen()
            else:
                self.push_screen(HelpScreen(id=HELP_SCREEN_ID))
                self.notify("Help Screen")
        except:
            None

    def key_ctrl_s(self):

        try:
            focused = self.focused
            if focused and focused.id == "text_editor":
                return
            if self.screen_stack[-1].id != SETTINGS_SCREEN_ID:
                self.push_screen(Settings(id=SETTINGS_SCREEN_ID))
            else:
                self.pop_screen()
        except Exception as e:
            logger.error(
                f"{e} Function: {self.key_ctrl_s.__name__} in {Path(__file__).name}"
            )
            None

    def key_escape(self):
        try:
            if self.screen_stack[-1].id != HOME_SCREEN_ID:
                self.pop_screen()
        except Exception as e:
            logger.error(
                f"{e} Function: {self.key_escape.__name__} in {Path(__file__).name}"
            )

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
