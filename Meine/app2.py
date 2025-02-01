from textual.app import App, SystemCommand
from textual.command import Provider, Hits, Hit
from pathlib import Path
from functools import partial
from typing import ClassVar

from Meine.logger_config import logger
from Meine.exceptions import InfoNotify
from Meine.Screens.settings import Settings, NameGetterScreen
from Meine.Screens.help import HelpScreen
from Meine.Screens.home import HomeScreen
from Meine.Actions.system import System
from Meine.utils.file_editor import add_custom_path_expansion

# Constants for screen IDs and common strings
HOME_SCREEN_ID = "home"
HELP_SCREEN_ID = "help_screen"
SETTINGS_SCREEN_ID = "settings"
CUSTOM_PATH_COMMAND = "Add custom path expansion"
CUSTOM_PATH_HELP = "Add a custom path expansion"


class CustomCommand(Provider):
    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)
        if score := matcher.match(CUSTOM_PATH_COMMAND):
            yield Hit(
                score,
                matcher.highlight(CUSTOM_PATH_COMMAND),
                partial(
                    self.app.push_screen,
                    NameGetterScreen(
                        title=CUSTOM_PATH_COMMAND,
                        callback=add_custom_path_expansion
                    )
                ),
                help=CUSTOM_PATH_HELP
            )


class MeineAI(App[None]):
    COMMANDS: ClassVar[set[type[Provider]]] = App.COMMANDS | {CustomCommand}

    async def on_mount(self) -> None:
        await self.push_screen(HomeScreen(id=HOME_SCREEN_ID))

    def get_system_commands(self, screen):
        yield from super().get_system_commands(screen)
        yield SystemCommand("settings", "Open settings", self.key_ctrl_s)
        yield SystemCommand("help", "Open help screen", self.key_ctrl_k)
        yield SystemCommand("shutdown", "Shutdown system", self.safe_shutdown)
        yield SystemCommand("reboot", "Reboot system", self.safe_reboot)

    def _handle_screen_transition(self, screen_type, screen_id):
        """Helper method for screen transitions."""
        try:
            if isinstance(self.screen, screen_type):
                self.pop_screen()
            else:
                self.push_screen(screen_type(id=screen_id))
        except Exception as e:
            logger.error(f"{e} in screen transition to {screen_id}")
            self.notify("Error changing view", severity="error")

    def key_ctrl_k(self) -> None:
        self._handle_screen_transition(HelpScreen, HELP_SCREEN_ID)

    def key_ctrl_s(self) -> None:
        self._handle_screen_transition(Settings, SETTINGS_SCREEN_ID)

    def key_escape(self) -> None:
        try:
            if not isinstance(self.screen, HomeScreen):
                self.pop_screen()
        except Exception as e:
            logger.error(f"Error handling escape: {e}")
            self.notify("Error closing view", severity="error")

    def _handle_system_operation(self, operation, success_message):
        """Helper for shutdown/reboot operations."""
        try:
            sys = System()
            getattr(sys, operation)()
            self.notify(success_message)
            self.set_timer(60, self.exit)  # 60 seconds = 1 minute
        except InfoNotify as e:
            self.notify(str(e))
            if "Minute" in str(e):
                self.set_timer(60, self.exit)
        except Exception as e:
            logger.error(f"System operation failed: {e}")
            self.notify("Operation failed", severity="error")

    def safe_shutdown(self) -> None:
        self._handle_system_operation("ShutDown", "System shutting down in 1 minute...")

    def safe_reboot(self) -> None:
        self._handle_system_operation("Reboot", "System rebooting in 1 minute...")



def run2():
    MeineAI().run()


