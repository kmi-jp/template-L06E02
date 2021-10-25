import pytest

from data.index import Index
from data.series import Series
from data.dataframe import DataFrame


input_text=""",names,salary,cash flow
user 1,Lukas Novak,20000,-100
user 2,Petr Pavel,300000,10000
user 3,Pavel Petr,20000,-2000
user 4,Ludek Skocil,50000,1100"""


def test_dataframe():
    users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

    salaries = Series([20000, 300000, 20000, 50000], index=users)
    names = Series(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"], index=users)
    cash_flow = Series([-100, 10000, -2000, 1100], index=users)

    columns = Index(["names", "salary", "cash flow"])
    data = DataFrame([names, salaries, cash_flow], columns=columns)

    assert data.columns == columns
    assert data.values == [names, salaries, cash_flow]
    assert isinstance(data.values, list)
    assert data.get("salary") == salaries
    assert data.get("cash flow").max() == 10000
    assert data.get("wrong key") == None


def test_str_repr():
    users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

    salaries = Series([20000, 300000, 20000, 50000], index=users)
    names = Series(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"], index=users)
    cash_flow = Series([-100, 10000, -2000, 1100], index=users)

    columns = Index(["names", "salary", "cash flow"])
    data = DataFrame([names, salaries, cash_flow], columns=columns)

    assert str(data) == "DataFrame(4, 3)"
    assert repr(data) == "DataFrame(4, 3)"


def test_shape():
    users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

    salaries = Series([20000, 300000, 20000, 50000], index=users)
    names = Series(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"], index=users)
    cash_flow = Series([-100, 10000, -2000, 1100], index=users)

    columns = Index(["names", "salary", "cash flow"])
    data = DataFrame([names, salaries, cash_flow], columns=columns)

    assert data.shape == (4, 3)


def test_from_csv():
    data = DataFrame.from_csv(input_text)

    assert data.columns.labels == ["names", "salary", "cash flow"]

    assert list(data.values[0].values) == list(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"])
    assert data.values[0].index.labels == ["user 1", "user 2", "user 3", "user 4"]
    assert list(data.values[1].values) == list(map(str, [20000, 300000, 20000, 50000]))
    assert data.values[1].index.labels == ["user 1", "user 2", "user 3", "user 4"]
    assert list(data.values[2].values) == list(map(str, [-100, 10000, -2000, 1100]))
    assert data.values[2].index.labels == ["user 1", "user 2", "user 3", "user 4"]

    assert data.get("salary").apply(int).sum() == sum([20000, 300000, 20000, 50000])


def test_empty_dataframe():
    with pytest.raises(ValueError):
        DataFrame([])


def test_empty_columns():
    users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

    salaries = Series([20000, 300000, 20000, 50000], index=users)
    names = Series(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"], index=users)
    cash_flow = Series([-100, 10000, -2000, 1100], index=users)

    data = DataFrame([names, salaries, cash_flow])

    assert data.columns.labels == Index(range(3)).labels
    assert data.values == [names, salaries, cash_flow]
    assert data.get(1) == salaries
    assert data.get(2).max() == 10000


@pytest.mark.parametrize(
    "function",
    [
        DataFrame,
        DataFrame.from_csv,
        DataFrame.get,
        DataFrame.shape
    ],
)
def test_docstrings(function):
    assert function.__doc__ is not None
