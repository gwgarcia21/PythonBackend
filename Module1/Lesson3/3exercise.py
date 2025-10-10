"""3. Hybrid Approach: Design a system that uses 
both asyncio and multiprocessing. The system should 
fetch data from multiple APIs concurrently using asyncio 
and then process the data in parallel using multiprocessing."""

import requests
import time
import aiohttp
import multiprocessing
import asyncio
import math

def fetch_data(years_ago=1):
    # Par e intervalo desejado
    symbol = "BTCBRL"
    interval = "1w"

    # Timestamp do último ano até agora
    end_time = int(time.time() * 1000)  # agora (em ms)
    start_time = end_time - years_ago * 365 * 24 * 60 * 60 * 1000  # 2 anos atrás

    # URL da API
    url = "https://api.binance.com/api/v3/klines"

    # Parâmetros da requisição
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_time,
        "endTime": end_time,
        "limit": 1000
    }

    # Requisição à API
    response = requests.get(url, params=params)
    data = response.json()
    return data

async def fetch_data_async(years_ago=1):
    # Par e intervalo desejado
    symbol = "BTCBRL"
    interval = "1w"

    # Timestamp do último ano até agora
    end_time = int(time.time() * 1000)  # agora (em ms)
    start_time = end_time - years_ago * 365 * 24 * 60 * 60 * 1000  # 2 anos atrás

    # URL da API
    url = "https://api.binance.com/api/v3/klines"

    # Parâmetros da requisição
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_time,
        "endTime": end_time,
        "limit": 1000
    }

    # Requisição à API
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            return data

def get_max(data):
    max = 0.0
    for candle in data:
        time.sleep(0.025)
        high = float(candle[2])
        if high > max:
            max = high
    return max

def split_into_blocks(data, block_size):
    return [data[i:i + block_size] for i in range(0, len(data), block_size)]

def main():
    print("--- Standard")
    start_time = time.time()
    data1 = fetch_data(1)
    data2 = fetch_data(2)
    data3 = fetch_data(3)
    results = [
        get_max(data1),
        get_max(data2),
        get_max(data3)
    ]
    end_time = time.time()
    print(f"Results: {results}")
    print(f"Total time taken: {end_time - start_time:.4f} seconds")

async def main_async():
    print("--- Asyncio")
    start_time = time.time()
    task1 = asyncio.create_task(fetch_data_async(1))
    task2 = asyncio.create_task(fetch_data_async(2))
    task3 = asyncio.create_task(fetch_data_async(3))
    data1 = await task1
    data2 = await task2
    data3 = await task3
    results = [
        get_max(data1),
        get_max(data2),
        get_max(data3)
    ]
    end_time = time.time()
    print(f"Results: {results}")
    print(f"Total time taken: {end_time - start_time:.4f} seconds")

async def main_multiprocess_async():
    print("--- Multiprocessing")
    start_time = time.time()
    task1 = asyncio.create_task(fetch_data_async(1))
    task2 = asyncio.create_task(fetch_data_async(2))
    task3 = asyncio.create_task(fetch_data_async(3))
    data1 = await task1
    data2 = await task2
    data3 = await task3
    results = [
        multiprocess_get_max(data1),
        multiprocess_get_max(data2),
        multiprocess_get_max(data3)
    ]
    end_time = time.time()
    print(f"Results: {results}")
    print(f"Total time taken: {end_time - start_time:.4f} seconds")

def multiprocess_get_max(data):
    cpu_count = multiprocessing.cpu_count()
    #print("CPU Count: ", cpu_count)
    block_size = int(len(data) / cpu_count)
    #print("Block size: ", block_size)
    split_data = split_into_blocks(data, block_size)
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(get_max, split_data)
    return max(results)

if __name__ == "__main__":
    main()
    asyncio.run(main_async())
    asyncio.run(main_multiprocess_async())