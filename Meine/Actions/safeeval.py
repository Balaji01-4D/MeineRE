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

allowedfunc: dict[str] = {'abb':a}


def main():
    x = input('>>>')
    print(SafeEval(x,allowedfunc))


if __name__ == '__main__':
    main()