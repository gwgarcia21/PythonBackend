import asyncio
import aiohttp
import time

async def fetch_url(session, url):
    start_time = time.time()
    print(f"Fetching {url}")
    try:
        async with session.get(url) as response:
            end_time = time.time()
            print(f"Time taken to fetch {url}: {end_time - start_time:.2f} seconds")
            return await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

async def main():
    urls = [
        "https://www.example.com",
        "https://www.google.com",
        "https://www.python.org",
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    for url, result in zip(urls, results):
        if result:
            print(f"Successfully fetched {url}")
        else:
            print(f"Failed to fetch {url}")

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f} seconds")