from progress_passthrough.utils import optional_len


class A:
    pass


class B:
    def __len__(self):
        return "broken"


def test_optional_len():
    optional_len([1, 2, 3]) == 3
    optional_len(A()) is None
    optional_len(B()) is None
