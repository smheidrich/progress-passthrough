# progress-passthrough

[![pipeline status](https://gitlab.com/smheidrich/progress-passthrough/badges/main/pipeline.svg?style=flat-square)](https://gitlab.com/smheidrich/progress-passthrough/-/commits/main)
[![codecov](https://codecov.io/gl/smheidrich/progress-passthrough/branch/main/graph/badge.svg?token=GBYVO057JT)](https://codecov.io/gl/smheidrich/progress-passthrough)
[![docs](https://img.shields.io/badge/docs-online-brightgreen?style=flat-square)](https://smheidrich.gitlab.io/progress-passthrough/)

Utilities to pass progress information through nested iterators.


## Example

The use case which inspired this is using progress bars like
[tqdm](https://github.com/tqdm/tqdm>) on "filtering generators" (think `(x for
x in l if some_condition(x))`) and wanting the progress to follow the iteration
over the inner (unfiltered) iterable instead of the filtered iterations.

Consider e.g.:

```python
from dataclasses import dataclass
from time import sleep
from tqdm import tqdm

@dataclass
class slow_range:
  """
  Range with simulated delay so progress bar doesn't fill up instantly.
  """
  n: int

  def __iter__(self):
     for x in range(self.n):
        sleep(0.01)
        yield x

  def __len__(self):
     return self.n

r = slow_range(100)

filtering_gen = (x for x in r if x % 37 == 0)

results = list(tqdm(filtering_gen))
```

This a) doesn't produce a progress bar because the length of the generator
output isn't known and b) even if it did, it would be choppier than it needs to
be because only filtered iterations move the bar, not iterations of the
original source iterable (`r`).

This library allows solving the issue in a generic manner that does not tie the
user down to a specific progress bar:

```python
from progress_passthrough.iterator_wrappers import wrap_source

r = slow_range(100)

# wrap r in several wrappers that together provide the functionality of this
# library (see below)
source_preserving_r = wrap_source(r)

# construct a generator and wrap it so that the original iterable (r) can
# still be accessed
filtering_gen = source_preserving_r.wrap(
   x for x in source_preserving_r if x % 31337 == 0
)

# attach a callback which updates tqdm on each iteration of r to one of the
# inner wrappers around it
with tqdm(total=len(filtering_gen.source)) as t:
 filtering_gen.source.callbacks.append(t.update)
 results = list(filtering_gen)
```


## Installation

```bash
pip install git+https://gitlab.com/smheidrich/progress-passthrough
```
