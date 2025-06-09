import multiprocessing
from PIL import Image
import time
import os

def process_image(image_path):
    print(f"Processing {image_path} in process {multiprocessing.current_process().name}")
    try:
        img = Image.open(image_path)
        # Simulate some image processing (e.g., resizing)
        img = img.resize((500, 500))
        img.save(f"processed_{os.path.basename(image_path)}")
        time.sleep(1)  # Simulate CPU-bound processing
        return f"Processed {image_path}"
    except Exception as e:
        return f"Error processing {image_path}: {e}"

def main():
    image_paths = [
        r"C:\Users\User\Pictures\Plotter Arts\duende.jpg",
        r"C:\Users\User\Pictures\Plotter Arts\zendaya.png",
        r"C:\Users\User\Pictures\Plotter Arts\spongebob.jpg",
    ]

    # Create dummy image files
    for path in image_paths:
        if not os.path.exists(path):
            img = Image.new('RGB', (1000, 1000), color='white')
            img.save(path)

    start_time = time.time()

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(process_image, image_paths)

    end_time = time.time()

    for result in results:
        print(result)
    print(f"Total time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()