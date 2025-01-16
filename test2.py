import asyncio
from Meine.Actions.file import File

async def cancel_me():

    print("cancel me() before sleeping")

    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print("cancel me() cancel sleep")
        raise
    finally:
        print('cancel me(): after sleep')



async def fact(name: str,num: int)-> int:
    print(f'{name} started')
    f = 1
    for i in range(2,num+1):
        await asyncio.sleep(1)
        f *= i
    print(f'{name} done')

    return f

async def main():

    task = asyncio.create_task(cancel_me())

    await asyncio.sleep(5)

    print(task.get_name())
    a = input(">> yes or no :")
    if (a == 'y'):
        task.cancel()
    else :
        None
    try:
        await task
    except asyncio.CancelledError:
        print("main(): cancel me is cancelled now")
    finally:
        print(task.cancelled())

if __name__ == '__main__':
    asyncio.run(main())
    