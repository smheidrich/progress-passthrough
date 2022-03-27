from progress_passthrough.iterator_wrappers import (
    IteratorWrapper,
    AttachedLengthIterator,
    CallbackIterator,
    wrap_source,
    wrap_source_len,
)
from unittest.mock import Mock


def test_iterator_wrapper_on_iterable():
    it = range(10)
    w = IteratorWrapper(it)
    assert len(w) == len(range(10))
    assert list(w) == list(range(10))


def test_iterator_wrapper_on_iterator():
    it = range(10).__iter__()
    w = IteratorWrapper(it)
    assert list(w) == list(range(10))


def test_attached_length_iterator():
    it = (x for x in range(10) if x % 2 == 0)
    w = AttachedLengthIterator(it, 3)  # give it a wrong length on purpose
    assert len(w) == 3
    assert list(w) == [0, 2, 4, 6, 8]


def test_callback_iterator_on_iterable():
    mock_cb = Mock()
    inner_it = range(10)
    w = CallbackIterator(inner_it)
    w.callbacks.append(mock_cb)
    outer_it = (x for x in w if x % 2 == 0)
    assert len(w) == 10
    assert list(outer_it) == [0, 2, 4, 6, 8]
    assert mock_cb.call_count == 10


def test_callback_iterator_on_iterator():
    mock_cb = Mock()
    inner_it = (x for x in range(10))
    w = CallbackIterator(inner_it)
    w.callbacks.append(mock_cb)
    outer_it = (x for x in w if x % 2 == 0)
    assert list(outer_it) == [0, 2, 4, 6, 8]
    assert mock_cb.call_count == 10


# test convenience functions


def test_wrap_source():
    mock_cb = Mock()
    inner_it = range(10)
    w = wrap_source(inner_it)
    w.source.callbacks.append(mock_cb)
    outer_it = w(x for x in w if x % 2 == 0)
    assert len(w.source) == 10
    assert list(outer_it) == [0, 2, 4, 6, 8]
    assert mock_cb.call_count == 10


def test_wrap_source_len():
    mock_cb = Mock()
    inner_it = (x for x in range(10))
    w = wrap_source_len(inner_it, 10)
    w.source.callbacks.append(mock_cb)
    outer_it = w(x for x in w if x % 2 == 0)
    assert len(w.source) == 10
    assert list(outer_it) == [0, 2, 4, 6, 8]
    assert mock_cb.call_count == 10
