import time
from typing import Callable


def measure_time(func: Callable[[], float], ntimes: int = 1) -> float | int:
    ret: float | int = -1

    start = time.time()
    for _ in range(ntimes):
        ret = func()
    dur = time.time() - start

    print(f"Duration: {(dur / ntimes) * 1000}ms")
    return ret

