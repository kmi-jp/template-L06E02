import statistics
import pytest

from data.index import Index
from data.series import Series

input_text = """user 1,user 2,user 3,user 4
Lukas Novak,Petr Pavel,Pavel Petr,Ludek Skocil
"""

def test_series():
    values = [20000, 300000, 20000, 50000]
    idx = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

    salaries = Series(values=values, index=idx)

    assert salaries.values == values
    assert isinstance(salaries.values, list)
    assert salaries.index == idx


def test_from_csv():
    data = Series.from_csv(input_text)

    assert data.index.labels == ["user 1", "user 2", "user 3", "user 4"]
    assert list(data.values) == list(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"])


def test_str_repr():
    users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")
    salaries = Series([20000, 300000, 20000, 50000], index=users)

    expected = """user 1\t20000
user 2\t300000
user 3\t20000
user 4\t50000"""

    assert repr(salaries) == expected
    assert str(salaries) == expected


def test_empty_index():
    values = [20000, 300000, 20000, 50000]
    salaries = Series(values)

    assert salaries.index.labels == Index(range(len(values))).labels


def test_series_get():
    values = [20000, 300000, 20000, 50000]
    idx = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

    salaries = Series(values=values, index=idx)

    assert salaries.get("user 2") == values[1]
    assert salaries.get("wrong key") == None


def test_series_sum():
    values = [20000, 300000, 20000, 50000]
    idx = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

    salaries = Series(values=values, index=idx)

    assert salaries.sum() == sum(values)


def test_series_max():
    values = [20000, 300000, 20000, 50000]
    idx = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

    salaries = Series(values=values, index=idx)

    assert salaries.max() == max(values)


def test_series_min():
    values = [20000, 300000, 20000, 50000]
    idx = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

    salaries = Series(values=values, index=idx)

    assert salaries.min() == min(values)


def test_series_mean():
    values = [20000, 300000, 20000, 50000]
    idx = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

    salaries = Series(values=values, index=idx)

    assert salaries.mean() == statistics.mean(values)


def test_series_apply():
    values = [20000, 300000, 20000, 50000]
    idx = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

    salaries = Series(values=values, index=idx)

    def squared(a):
        """Returns squared number"""
        return a ** 2

    result = salaries.apply(squared)

    assert salaries != result
    assert salaries is not result
    assert result.values == list(map(squared, values))


def test_series_abs():
    values = [20000, -300000, 20000, -50000]
    idx = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

    salaries = Series(values=values, index=idx)

    result = salaries.abs()

    assert salaries != result
    assert salaries is not result
    assert result.values == list(map(abs, values))


def test_empty_series():
    with pytest.raises(ValueError):
        Series(values=[])


@pytest.mark.parametrize(
    "values,labels",
    [
        ([20000, 300000, 20000], ["user 1"]),
        ([20000], ["user 1", "user 2"]),
    ],
)
def test_values_index_length_mismatch(values, labels):
    idx = Index(labels, name="names")

    with pytest.raises(ValueError):
        Series(values=values, index=idx)