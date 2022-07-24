import pytest

from data.index import Index
from data.series import Series
from data.dataframe import DataFrame


@pytest.fixture
def users():
    return Index(["user 1", "user 2", "user 3", "user 4"], name="names")


@pytest.fixture
def names(users):
    return Series(
        ["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"], index=users
    )


@pytest.fixture
def salaries(users):
    return Series([20000, 300000, 20000, 50000], index=users)


@pytest.fixture
def cash_flow(users):
    return Series([-100, 10000, -2000, 1100], index=users)


@pytest.fixture
def columns():
    return Index(["names", "salary", "cash flow"])


def test_str_repr(names, salaries, cash_flow, columns):
    data = DataFrame([names, salaries, cash_flow], columns=columns)

    assert str(data) == "DataFrame(4, 3)"
    assert repr(data) == "DataFrame(4, 3)"


def test_shape(names, salaries, cash_flow, columns):
    data = DataFrame([names, salaries, cash_flow], columns=columns)

    assert data.shape == (4, 3)


def test_from_csv():
    input_text = """,names,salary,cash flow
user 1,Lukas Novak,20000,-100
user 2,Petr Pavel,300000,10000
user 3,Pavel Petr,20000,-2000
user 4,Ludek Skocil,50000,1100"""

    data = DataFrame.from_csv(text=input_text)

    assert data.columns.labels == ["names", "salary", "cash flow"]

    assert list(data.values[0].values) == list(
        ["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"]
    )
    assert data.values[0].index.labels == ["user 1", "user 2", "user 3", "user 4"]
    assert list(data.values[1].values) == list(map(str, [20000, 300000, 20000, 50000]))
    assert data.values[1].index.labels == ["user 1", "user 2", "user 3", "user 4"]
    assert list(data.values[2].values) == list(map(str, [-100, 10000, -2000, 1100]))
    assert data.values[2].index.labels == ["user 1", "user 2", "user 3", "user 4"]

    assert data.get("salary").apply(int).sum() == sum([20000, 300000, 20000, 50000])


@pytest.mark.parametrize(
    "function",
    [DataFrame, DataFrame.from_csv, DataFrame.get, DataFrame.shape],
)
def test_docstrings(function):
    assert function.__doc__ is not None
