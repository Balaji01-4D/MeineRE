import time
a=time.time()
from rich.console import Console
import re
import os
import prime


CONSOLE = Console()




a1 = time.time()
print(f"importing and instance making time {a1-a:.4f}")
with CONSOLE.status(f"[bold cyan]Loading spaCy model...", spinner='dots'):
    import spacy
    nlp = spacy.load('en_core_web_sm') 

b=time.time()
print(f"modal loading time {b-a1:.2f}")
def AI(Command: str) -> str | dict[str]:
    doc = nlp(Command)
    CDict = {}
    # Labels , Texts = [],[]
    # for ent in doc.ents:
    #     Labels.append(ent.label_)
    #     Texts.append(ent.text)
    # CDict = op.other.CMDMapper(Labels,Texts)
    # Action:str = CDict['ACTION']
    # Action = Action.lower()
    # return Action,CDict
   



def Cli() -> None | str | dict:
    while True:
        Command: str = input(">>> ")
        b=time.time()
        try:
        
            if (re.fullmatch(r"[0-9+\-*/%(). ]+",Command)):
                print(eval(Command))

            elif bool(re.search(r"\b[sS]hell\b",Command)):
                sys:str = re.sub(r"\b[sS]hell\b","",Command)
                print("system command",sys)
                os.system(sys)

            else :
                AI(Command)

        except Exception as e:

            print("error: ",e)



def main():

    Action,cdict = Cli()

    prime.WHatAction(Action,cdict)





c = time.time()
print(f"End time {c-b:.5f}")