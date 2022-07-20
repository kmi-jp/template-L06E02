import operator

import pytest

from data.index import Index
from data.series import Series


@pytest.fixture
def salaries_data():
    return [20000, 300000, 20000, 50000]


@pytest.fixture
def cash_flow_data():
    return [-100, 10000, -2000, 1100]


@pytest.fixture
def users_data():
    return ["user 1", "user 2", "user 3", "user 4"]


@pytest.fixture
def idx(users_data):
    return Index(labels=users_data, name="names")


@pytest.fixture
def salaries(salaries_data, idx):
    return Series(values=salaries_data, index=idx)


@pytest.fixture
def cash_flow(cash_flow_data, idx):
    return Series(values=cash_flow_data, index=idx)


def test_len(salaries):
    assert len(salaries) == 4


def test_shape(salaries):
    assert salaries.shape == (4,)


def test_from_csv(users_data):
    input_text = """user 1,user 2,user 3,user 4
Lukas Novak,Petr Pavel,Pavel Petr,Ludek Skocil
"""

    data = Series.from_csv(text=input_text, separator=",")

    assert data.index.labels == users_data
    assert list(data.values) == list(
        ["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"]
    )


def test_str_repr(salaries):
    expected = """user 1\t20000
user 2\t300000
user 3\t20000
user 4\t50000"""

    assert repr(salaries) == expected
    assert str(salaries) == expected


def test_apply_operator(salaries, cash_flow, salaries_data, cash_flow_data):
    result = salaries._apply_operator(other=cash_flow, operator=operator.add)

    expected = list(
        map(lambda x: operator.add(x[0], x[1]), zip(salaries_data, cash_flow_data))
    )

    assert result.values == expected
    assert result.index.labels == salaries.index.labels == cash_flow.index.labels


def test_apply_operator_exception():
    with pytest.raises(ValueError):
        Series(values=[1, 2])._apply_operator(
            other=Series(values=[1]), operator=operator.add
        )


@pytest.mark.parametrize(
    "operator",
    [
        (operator.add),
        (operator.sub),
        (operator.mul),
        (operator.truediv),
        (operator.floordiv),
        (operator.mod),
        (operator.pow),
    ],
)
def test_operators(operator, salaries, cash_flow, salaries_data, cash_flow_data):
    expected = list(
        map(lambda x: operator(x[0], x[1]), zip(salaries_data, cash_flow_data))
    )

    result = operator(salaries, cash_flow)

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
def test_operators_exception(operator, salaries):
    with pytest.raises(TypeError):
        operator(salaries, 1)


def test_round():
    assert (
        round(Series(values=[1.252, 2.23231312]), 2).values
        == Series(values=[1.25, 2.23]).values
    )


@pytest.mark.parametrize(
    "function",
    [Series, Series.get, Series.from_csv, Series.shape],
)
def test_docstrings(function):
    assert function.__doc__ is not None
