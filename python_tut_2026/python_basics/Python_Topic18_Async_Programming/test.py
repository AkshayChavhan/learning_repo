import asyncio


# async def makeCoffie():
#     print("Coffie making started")
#     await asyncio.sleep(2)
#     print("Coffie making completed")

# asyncio.run(makeCoffie())

# -----------------------------------------


async def fetch_Data(name , seconds):
    print(f"Fetching started {name}")
    await asyncio.sleep(seconds)
    print(f"Fetching completed {name}")
    return name


# asyncio.run(fetch_Data("Akshay",5))

# ❌
# Sequential — one after another (total: 3 seconds)
async def slow():
    await fetch_Data("A", 3)
    await fetch_Data("B", 3)
    await fetch_Data("C", 3)

# asyncio.run(slow()) 



async def fast():
    await asyncio.gather(
        fetch_Data("A", 5),
        fetch_Data("B", 5),
        fetch_Data("C", 5),
    )

# asyncio.run(fast()) 