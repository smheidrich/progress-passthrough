from functools import partial
from unittest.mock import patch

import pytest
import tqdm.std

from progress_passthrough.iterator_wrappers import wrap_source
from progress_passthrough.tqdm import TqdmOnSource, TqdmPreferablyOnSource


@pytest.fixture()
def it():
    return range(100)


def test_tqdm_on_source(it):
    w = wrap_source(it)
    it2 = w(x for x in w if x % 2 == 50)
    with patch("tqdm.std.tqdm.update") as mock_update:
        t = TqdmOnSource(it2)
        assert t.total == 100
        assert mock_update.call_count == 0
        r = list(t)
        assert r == [x for x in range(100) if x % 2 == 50]
        assert mock_update.call_count == 100


def test_tqdm_preferably_on_source_with_source(it):
    w = wrap_source(it)
    it2 = w(x for x in w if x % 2 == 50)
    with patch("tqdm.std.tqdm.update") as mock_update:
        t = TqdmPreferablyOnSource(it2)
        assert t.total == 100
        assert mock_update.call_count == 0
        r = list(t)
        assert r == [x for x in range(100) if x % 2 == 50]
        assert mock_update.call_count == 100


def test_tqdm_preferably_on_source_without_source(it):
    it2 = (x for x in it if x % 2 == 50)
    orig_iter = tqdm.std.tqdm.__iter__
    with patch("tqdm.std.tqdm.__iter__") as mock_iter:
        t = TqdmPreferablyOnSource(it2)
        mock_iter.side_effect = partial(orig_iter, t)
        assert t.total == None
        assert mock_iter.call_count == 0
        r = list(t)
        assert r == [x for x in range(100) if x % 2 == 50]
        assert mock_iter.call_count == 1
