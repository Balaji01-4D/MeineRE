def SafeEval(command: str,AllowedFunc: dict[str,callable] = {}) -> None|int|str:
    try:
        result = eval(command,AllowedFunc,{})
        return result
    except Exception as e:
        return e

def b():
    print("good mrng")


def a(*args) -> None:
    print('hello world')

allowedfunc: dict[str,callable] = {'a':a}

while True:
    cmd = input(">>>> ")
    print(SafeEval(cmd,allowedfunc))
