from rich.panel import Panel
from rich.style import Style
from rich import print as pp


st = Style()

hello = Panel("hello world",highlight=True,style=st)

pp(hello)
