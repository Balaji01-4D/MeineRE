from Meine.Screens.home import HomeScreen
from textual.app import App


class summa(App[None]):
    
    async def on_mount(self):
        await self.push_screen(HomeScreen())

def main():
    summa().run()


if __name__ == '__main__':
    main()