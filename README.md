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
Simply putting the `tqdm` call at the innermost level in such situations is
not always an option, e.g. if it's meant to be core application logic and
should therefore be interface-independent.

As a minimal example, consider e.g.:

```python
from tqdm import tqdm
# range with simulated delay so progress bar doesn't fill up instantly
from progress_passthrough.demo_utils import slow_range

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
   x for x in source_preserving_r if x % 37 == 0
)

# attach a callback which updates tqdm on each iteration of r to one of the
# inner wrappers around it, then iterate
with tqdm(total=len(filtering_gen.source)) as t:
 filtering_gen.source.callbacks.append(t.update)
 results = list(filtering_gen)
```

For more examples and the full API documentation, refer to the
[documentation](https://smheidrich.gitlab.io/progress-passthrough/).


## Installation

```bash
pip install git+https://gitlab.com/smheidrich/progress-passthrough
```
