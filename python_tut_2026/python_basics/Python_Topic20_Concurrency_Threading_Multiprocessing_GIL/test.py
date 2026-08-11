import threading


# Threads are lightweight and share the same memory. 
# Ideal when tasks spend their time waiting — network calls, file reads, DB queries. .start() launches, .join() waits for completion.

# def download(name):
#     print(f"Downloading {name}")
#     # ... waits on the network ...

# threads = []
# for name in ["a", "b", "c"]:
#     print(f"Running for {name}")
#     t = threading.Thread(target=download, args=(name,))
#     print(f"Thread start for {name}")
#     t.start()               # start the thread running
#     threads.append(t)

# for t in threads:
#     print(f"Thread join for {t}")
#     t.join()                # wait here until each thread finishes




from multiprocessing import Process

def crunch(n):
    total = sum(i**2 for i in range(n))   # heavy CPU work
    print(f" crunch for {total}")

processes = []
for _ in range(4):
    p = Process(target=crunch, args=(10**7,))
    print(f" Process started for {p}")
    p.start()               # each runs on its own CPU core
    processes.append(p)

for p in processes:
    print(f" Process joining for {p}")
    p.join()