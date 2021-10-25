import pytest

from data.index import Index


def test_index():
    test_labels = ["key 1", "key 2", "key 3", "key 4", "key 5"]

    idx = Index(labels=test_labels)
    values = [0, 1, 2, 3, 4]

    assert idx.labels == test_labels
    assert isinstance(idx.labels, list)
    assert values[idx.get_loc("key 2")] == 1
    assert idx.name == ""


def test_empty_labels():
    with pytest.raises(ValueError):
        Index([])


def test_nonempty_name():
    idx = Index(labels=["key 1", "key 2", "key 3", "key 4", "key 5"], name="index")

    assert idx.name == "index"


def test_invalid_key():
    with pytest.raises(KeyError):
        Index(["key 1"]).get_loc("key 2")


def test_label_duplicity():
    with pytest.raises(ValueError):
        Index(["key 1", "key 1", "key 3", "key 4", "key 5"])
    

@pytest.mark.parametrize(
    "function",
    [
        Index,
        Index.get_loc
    ],
)
def test_docstrings(function):
    assert function.__doc__ is not None
