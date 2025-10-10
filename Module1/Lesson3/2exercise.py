"""2. Multiprocessing Data Analysis: Create a program 
that uses multiprocessing to analyze a large dataset 
in parallel. Split the dataset into chunks and assign 
each chunk to a different process for analysis. Use a 
queue to collect the results from each process and 
combine them into a final result."""

import requests
import time
import datetime
import multiprocessing

def fetch_data():
    # Par e intervalo desejado
    symbol = "BTCBRL"
    interval = "1d"

    # Timestamp do último ano até agora
    end_time = int(time.time() * 1000)  # agora (em ms)
    start_time = end_time - 2 * 365 * 24 * 60 * 60 * 1000  # 2 anos atrás

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

def get_max(data):
    max = 0.0
    for candle in data:
        time.sleep(0.005)
        high = float(candle[2])
        if high > max:
            max = high
    return max

def split_into_blocks(data, block_size):
    return [data[i:i + block_size] for i in range(0, len(data), block_size)]

def main():
    print("--- Standard")
    data = fetch_data()
    start_time = time.time()
    results = get_max(data)
    end_time = time.time()
    print(f"Results: {results}")
    print(f"Total time taken: {end_time - start_time:.4f} seconds")

def main_multiprocess():
    print("--- Multiprocessing")
    data = fetch_data()
    cpu_count = multiprocessing.cpu_count()
    print("CPU Count: ", cpu_count)
    block_size = int(len(data) / cpu_count)
    print("Block size: ", block_size)
    split_data = split_into_blocks(data, block_size)
    start_time = time.time()
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(get_max, split_data)
    end_time = time.time()
    print(f"Results: {results}")
    print(f"Total time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
    main_multiprocess()

# Mostrar dados formatados (data, open, high, low, close)
# for candle in data:
#     ts = candle[0]
#     date = datetime.datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d')
#     open_price = candle[1]
#     high = candle[2]
#     low = candle[3]
#     close = candle[4]
#     print(f"{date}: Open={open_price}, High={high}, Low={low}, Close={close}")