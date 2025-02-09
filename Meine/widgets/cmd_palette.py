from functools import partial

from textual.command import Hit, Hits, Provider

from Meine.utils.file_editor import add_custom_path_expansion


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
                    self.app.NameGetterScreen(
                        title=f"{C}", callback=add_custom_path_expansion
                    ),
                ),
                help=f"adding a custom path expansions",
            )
