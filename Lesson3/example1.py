import asyncio
import time

async def fetch_data(url):
    print(f"Fetching data from {url}")
    # Simulate an I/O-bound operation (e.g., network request)
    await asyncio.sleep(2)  # Simulate waiting for 2 seconds
    print(f"Data fetched from {url}")
    return f"Data from {url}"

async def main():
    start_time = time.time()
    task1 = asyncio.create_task(fetch_data("https://example.com/api/data1"))
    task2 = asyncio.create_task(fetch_data("https://example.com/api/data2"))

    data1 = await task1
    data2 = await task2

    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f} seconds")
    print(f"Data 1: {data1}")
    print(f"Data 2: {data2}")

if __name__ == "__main__":
    asyncio.run(main())