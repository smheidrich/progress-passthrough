from progress_passthrough.iterator_wrappers import wrap_source
from progress_passthrough.tqdm import TqdmOnSource
from unittest.mock import patch


def test_tqdm_on_source():
    it = range(100)
    w = wrap_source(it)
    it2 = w(x for x in w if x % 2 == 50)
    with patch("tqdm.std.tqdm.update") as mock_update:
        t = TqdmOnSource(it2)
        assert t.total == 100
        assert mock_update.call_count == 0
        list(t)
        assert mock_update.call_count == 100
