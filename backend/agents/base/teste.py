import concurrent.futures
import time

def task(name):
    print(f"Task {name}: Starting...")
    time.sleep(2)  # Simulate I/O-bound operation
    print(f"Task {name}: Finished.")
    return f"Result from Task {name}"

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit tasks to the thread pool
        future1 = executor.submit(task, "A")
        future2 = executor.submit(task, "B")
        future3 = executor.submit(task, "C")

        # Retrieve results as they complete
        print(future1.result())
        print(future2.result())
        print(future3.result())