import abc
import logging
import logging.handlers
import os
import random
import time
import sys

from itertools import permutations
from typing import Iterable


logger = logging.getLogger(f"app_{os.getpid()}")


class Sorter(abc.ABC):
    def __init__(self) -> None:
        id = os.getpid()
        self.logger = logging.getLogger(f"app_{id}.{self.__class__.__name__}")

    @abc.abstractmethod
    def sort(self, data: list[float]) -> list[float]: ...


class BogoSort(Sorter):

    @staticmethod
    def is_sorted(data: tuple[float, ...]) -> bool:
        pairs: Iterable[tuple[float, float]] = zip(data, data[1:])
        return all(a <= b for a, b in pairs)

    def sort(self, data: list[float]) -> list[float]:
        self.logger.info("Sorting %d", len(data))
        start = time.perf_counter()

        ordering: tuple[float, ...] = tuple(data[:])
        permute_iter = permutations(data)

        steps = 0
        while not BogoSort.is_sorted(ordering):
            ordering = next(permute_iter)
            steps += 1

        duration = 1000 * (time.perf_counter() - start)
        self.logger.info(
            "Sorted %d items in %d steps, %.3f ms", len(data), steps, duration
        )
        return list(ordering)


def main(workload: int, sorter: Sorter = BogoSort()) -> int:
    total = 0
    for i in range(workload):
        samples = random.randint(3, 10)
        data = [random.random() for _ in range(samples)]
        ordered = sorter.sort(data)
        total += samples

    return total


if __name__ == "__main__":
    LOG_CATCHER_HOST, LOG_CATCHER_PORT = "localhost", 18842
    socket_handler = logging.handlers.SocketHandler(LOG_CATCHER_HOST, LOG_CATCHER_PORT)
    stream_handler = logging.StreamHandler(sys.stderr)
    logging.basicConfig(handlers=[socket_handler, stream_handler], level=logging.INFO)

    workload = random.randint(10, 20)
    logger.info("Sorting %d collections.", workload)
    start = time.perf_counter()
    samples = main(workload, BogoSort())
    end = time.perf_counter()
    logger.info("Sorted %d collections, took %f s.", workload, end - start)

    logging.shutdown()
