"""
Iterator wrappers that add features but pass iteration requests through.

The core of this library.
"""
from collections.abc import Iterable, Callable


class IteratorWrapper:
    """
    General iterator that wraps around an iterable.
    """

    def __init__(self, wrapped: Iterable):
        self.wrapped = wrapped

    def __iter__(self):
        self._iter = self.wrapped.__iter__()
        return self

    def __next__(self):
        return self._iter.__next__()

    def __len__(self):
        return len(self.wrapped)


class AttachedLengthIterator(IteratorWrapper):
    """
    Iterator wrapper to attach a length to an iterable that doesn't have one.

    Not strictly in the scope of this project, but often comes in handy in
    situations where one would use it, so included here.
    """

    def __init__(self, wrapped, length):
        super().__init__(wrapped)
        self.length = length

    def __len__(self):
        return self.length


class CallbackIterator(IteratorWrapper):
    """
    Iterator wrapper to call a list of callbacks on each iteration.
    """

    def __init__(self, wrapped: Iterable, callbacks: list[Callable] = None):
        super().__init__(wrapped)
        self.callbacks = callbacks if callbacks is not None else []

    def __next__(self):
        # has to be in this order to avoid an erroneous callback on
        # StopIteration
        r = super().__next__()
        for callback in self.callbacks:
            callback()
        return r


class SourcePreservingIterator(IteratorWrapper):
    """
    Iterator wrapper to keep track of an ultimate source iterable when nesting.
    """

    def __init__(self, wrapped: Iterable, source: Iterable = None):
        super().__init__(wrapped)
        self.source = source

    def wrap(self, wrapped: Iterable):
        """
        Wrap another iterable in a `~.SourcePreservingIterator` with the same
        source.
        """
        pt = self.__class__(wrapped, source=self.source)
        return pt

    def __call__(self, wrapped: Iterable):
        """
        Shorthand for wrap().
        """
        return self.wrap(wrapped)


def wrap_source(wrapped: Iterable):
    """
    Conveniently apply `~.SourcePreservingIterator` and `~.CallbackIterator`.

    First wraps the iterator in a `~.CallbackIterator` and then wraps that in a
    `~.SourcePreservingIterator`. The `~.CallbackIterator` is set as the source
    so users can attach callbacks.
    """
    cbi = CallbackIterator(wrapped)
    spi = SourcePreservingIterator(cbi, source=cbi)
    return spi


def wrap_source_len(wrapped: Iterable, length):
    """
    Same as wrap_source but also attach a length.

    The `~.AttachedLengthIterator` will be the innermost wrapper around the
    supplied iterator.
    """
    ali = AttachedLengthIterator(wrapped, length)
    return wrap_source(ali)
