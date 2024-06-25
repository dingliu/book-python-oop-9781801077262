import asyncio
import random


async def random_sleep(counter: int) -> None:
    delay = random.random() * 5
    print(f"[{counter}] Sleeping for {delay:.2f} seconds.")
    await asyncio.sleep(delay)
    print(f"[{counter}] awakens, refreshed.")


async def sleepers(how_many: int) -> None:
    print(f"Creating [{how_many}] random sleepers.")

    tasks = [asyncio.create_task(random_sleep(i)) for i in range(how_many)]

    print(f"Waiting for [{how_many}] random sleepers to wake up.")
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(sleepers(5))
    print("All sleepers have awakened.")
