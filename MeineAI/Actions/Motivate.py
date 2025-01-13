from random import randint
from rich.console import Console
from rich.theme import Theme
color = Theme({
    'info':'blue',
    'mag':'bold italic magenta',
    'motivate':'bold italic red'
})
console = Console(theme=color)

def Motivate() -> None:

    with open('MeineAI/Resources/qoutes.txt','r') as qoutes:
        Lines = qoutes.readlines()
        console.print(Lines[randint(0,len(Lines)-1)],style='motivate')

def AddQoute(quote: str) -> None:
    with open('MeineAI/Resources/qoutes.txt','a') as quotes:
        quotes.write(quote+"\n")

console.print('hellow',style='info')