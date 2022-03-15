# progress-passthrough

[![pipeline status](https://gitlab.com/smheidrich/progress-passthrough/badges/main/pipeline.svg?style=flat-square)](https://gitlab.com/smheidrich/progress-passthrough/-/commits/main)
[![codecov](https://img.shields.io/codecov/c/gl/smheidrich/progress-passthrough?style=flat-square&token=TODO)](https://codecov.io/gl/smheidrich/progress-passthrough)
[![docs](https://img.shields.io/badge/docs-online-brightgreen?style=flat-square)](https://smheidrich.gitlab.io/progress-passthrough/)

Utilities to pass progress information through nesting levels.


## Example

The use case which inspired this is using progress bars like
[`tqdm`](https://github.com/tqdm/tqdm) on filtering generators but wanting the
bar to progress as determined by the original iterable the generator iterates
over.

Consider e.g.:

```python
from tqdm import tqdm

r = range(1000000)

filtering_gen = (x for x in r if x % 31337 == 0)

# this a) doesn't produce a progress bar because the length of the generator
# isn't known and b) even if it did, it would be choppier than it needs to be
# because only result iterations move the bar, not iterations of the original
# source iterable (r)
results = list(tqdm(filtering_gen))
```

With the help of this library, the issue can be resolved by the author of the
generator in a generic manner that does not tie the user down to a specific
progress bar:

```python
from tqdm import tqdm
from progress_passthrough.iterator_wrappers import wrap_source

r = range(1000000)

# wrap r in a wrapper that in turn allows wrapping generators involving it in
# wrappers by which one can access it (r) and also allows attaching callbacks
# to be run on each iteration:
source_preserving_r = wrap_source(r)

# construct a generator making use of the aforementioned functionality
filtering_gen = source_preserving_r.wrap(
    x for x in source_preserving_r if x % 31337 == 0
)

# use the callback functionality to update tqdm progress on each iteration of
# the original source iterable (r)
with tqdm(total=len(filtering_gen.source)) as t:
  filtering_gen.source.callbacks.append(t.update)
  results = list(filtering_gen)
```


## Installation

```bash
pip install git+https://gitlab.com/smheidrich/progress-passthrough
```
