import statistics
import operator
from typing import Type

import pytest

from data.index import Index
from data.series import Series

input_text = """user 1,user 2,user 3,user 4
Lukas Novak,Petr Pavel,Pavel Petr,Ludek Skocil
"""

user_labels = ["user 1", "user 2", "user 3", "user 4"]
idx = Index(user_labels, name="names")
salaries_values = [20000, 300000, 20000, 50000]
salaries = Series(values=salaries_values, index=idx)
cash_flow_values = [-100, 10000, -2000, 1100]
cash_flow = Series(cash_flow_values, index=idx)


def test_series():
    assert salaries.values == salaries_values
    assert isinstance(salaries.values, list)
    assert salaries.index == idx


def test_from_csv():
    data = Series.from_csv(input_text)

    assert data.index.labels == user_labels
    assert list(data.values) == list(
        ["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"]
    )


def test_str_repr():
    expected = """user 1\t20000
user 2\t300000
user 3\t20000
user 4\t50000"""

    assert repr(salaries) == expected
    assert str(salaries) == expected


def test_shape():
    assert salaries.shape == (4,)


def test_empty_index():
    salaries = Series(salaries_values)

    assert salaries.index.labels == Index(range(len(salaries_values))).labels


def test_series_get():
    assert salaries.get("user 2") == salaries_values[1]
    assert salaries.get("wrong key") == None


def test_series_sum():
    assert salaries.sum() == sum(salaries_values)


def test_series_max():
    assert salaries.max() == max(salaries_values)


def test_series_min():
    assert salaries.min() == min(salaries_values)


def test_series_mean():
    assert salaries.mean() == statistics.mean(salaries_values)


def test_series_apply():
    def squared(a):
        """Returns squared number"""
        return a ** 2

    result = salaries.apply(squared)

    assert salaries != result
    assert salaries is not result
    assert result.values == list(map(squared, salaries_values))


def test_series_abs():
    result = salaries.abs()

    assert salaries != result
    assert salaries is not result
    assert result.values == list(map(abs, salaries_values))


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


def test_apply_operator():
    result = salaries._apply_operator(cash_flow, operator.add)

    expected = list(
        map(lambda x: operator.add(x[0], x[1]), zip(salaries_values, cash_flow_values))
    )

    assert result.values == expected
    assert result.index.labels == salaries.index.labels == cash_flow.index.labels


def test_apply_operator_exception():
    with pytest.raises(ValueError):
        Series([1, 2])._apply_operator(Series([1]), operator.add)


@pytest.mark.parametrize(
    "result,operator",
    [
        (salaries + cash_flow, operator.add),
        (salaries - cash_flow, operator.sub),
        (salaries * cash_flow, operator.mul),
        (salaries / cash_flow, operator.truediv),
        (salaries // cash_flow, operator.floordiv),
        (salaries % cash_flow, operator.mod),
        (salaries ** cash_flow, operator.pow),
    ],
)
def test_operators(result, operator):
    expected = list(
        map(lambda x: operator(x[0], x[1]), zip(salaries_values, cash_flow_values))
    )

    assert result.values == expected
    assert result.index.labels == salaries.index.labels == cash_flow.index.labels


@pytest.mark.parametrize(
    "operator",
    [
        operator.add,
        operator.sub,
        operator.mul,
        operator.truediv,
        operator.floordiv,
        operator.mod,
        operator.pow,
    ],
)
def test_operators_exception(operator):
    with pytest.raises(TypeError):
        operator(salaries, 1)


def test_round():
    assert round(Series([1.252, 2.23231312]), 2).values == Series([1.25, 2.23]).values


@pytest.mark.parametrize(
    "function",
    [
        Series,
        Series.from_csv,
        Series.get,
        Series.shape,
        Series.sum,
        Series.max,
        Series.min,
        Series.mean,
        Series.apply,
        Series.abs
    ],
)
def test_docstrings(function):
    assert function.__doc__ is not None