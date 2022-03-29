"""
Utilities for demonstrations, examples etc.
"""
from dataclasses import dataclass
from time import sleep


@dataclass
class slow_range:
    """
    Range with simulated delay so progress bars don't fill up instantly.
    """

    n: int
    delay: float = 0.01

    def __iter__(self):
        for x in range(self.n):
            sleep(self.delay)
            yield x

    def __len__(self):
        return self.n
