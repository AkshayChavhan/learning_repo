import time

def print_seperator(length: int = 60):
    print("=" * length)

def print_title(title:str):
    print_seperator()
    print(title)
    print_seperator()

def execution_time(start_time: float):
    print(f"\nExecution Time: {time.time() - start_time:.2f} seconds")