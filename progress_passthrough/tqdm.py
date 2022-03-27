"""
tqdm wrappers that make it compatible with this library.

Requires the `tqdm` extra to be installed.
"""
# ensure extra is installed
from pkg_resources import require
require("progress_passthrough[tqdm]")

from collections import ChainMap
from collections.abc import Iterable
from typing import Optional, Union

from tqdm import tqdm as _tqdm

from .iterator_wrappers import SourcePreservingIterator
from .utils import optional_len


class TqdmOnSource(_tqdm):
    """
    tqdm subclass that uses the iterator's source for progress information.
    """
    def __init__(
        self, iterable: Optional[SourcePreservingIterator] = None, **kwargs
    ):
        kwargs = _tqdm_kwargs_for_source(iterable, **kwargs)
        super().__init__(iterable=iterable, **kwargs)

    def __iter__(self):
        return _tqdm_iter_for_source(self)


class TqdmPreferablyOnSource(_tqdm):
    """
    tqdm subclass that uses the iterator's source progress if available.

    Falls back to using the iterator itself if it doesn't have source
    information (i.e., is not a `~.SourcePreservingIterator` instance).
    """
    def __init__(
        self,
        iterable: Optional[Union[SourcePreservingIterator, Iterable]] = None,
        **kwargs
    ):
        if isinstance(iterable, SourcePreservingIterator):
            kwargs = _tqdm_kwargs_for_source(iterable, **kwargs)
        super().__init__(iterable=iterable, **kwargs)

    def __iter__(self):
        if isinstance(self.iterable, SourcePreservingIterator):
            return _tqdm_iter_for_source(self)
        else:
            return super().__iter__()


def _tqdm_kwargs_for_source(
    iterable: Optional[SourcePreservingIterator] = None, **kwargs
) -> dict:
    if iterable is not None and "total" not in kwargs:
        length = optional_len(iterable.source)
        kwargs = ChainMap(dict(total=length), kwargs)
    return kwargs


def _tqdm_iter_for_source(tqdm_instance):
    iterable: SourcePreservingIterator = tqdm_instance.iterable
    with tqdm_instance as t:
        iterable.source.callbacks.append(lambda *a, **kw: t.update())
        for i, x in enumerate(iterable):
            yield x
