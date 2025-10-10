import multiprocessing
import time

def square(number):
    print(f"Squaring {number} in process {multiprocessing.current_process().name}")
    time.sleep(1)  # Simulate a CPU-bound operation
    return number * number

def main():
    numbers = [1, 2, 3, 4, 5]
    start_time = time.time()

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(square, numbers)

    end_time = time.time()

    print(f"Results: {results}")
    print(f"Total time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()