import asyncio


async def producer(queue: asyncio.Queue):
    for i in range(10):
        await asyncio.sleep(1)
        await queue.put(i)

    await queue.put(None)


async def consumer(queue: asyncio.Queue):
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break

        print(f"Consumed: {item}")
        queue.task_done()


async def main():
    queue = asyncio.Queue()
    tasks = [
        asyncio.create_task(producer(queue)),
        asyncio.create_task(consumer(queue)),
    ]

    await asyncio.gather(*tasks)
    await queue.join()


if __name__ == "__main__":
    asyncio.run(main())


""" Output:
Consumed: 0
Consumed: 1
Consumed: 2
Consumed: 3
Consumed: 4
Consumed: 5
Consumed: 6
Consumed: 7
Consumed: 8
Consumed: 9
"""
