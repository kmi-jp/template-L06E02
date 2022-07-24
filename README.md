# L06E02: Data 2
Balíček `data` z minulého semináře rozšiřte o následující funkcionalitu. Ve zdrojovém kódu urdžujte pořádek a metody seskupujte dle významu.

## Metoda `__len__`
Třídě `DataFrame`, `Series` a `Index` implementujte metodu `__len__` obsluhující volání funkce `len()`. V případě třídy `Series` a `Index` se jedná o počet prvků, v případě `DataFrame` o počet sloupců.

## Vlastnost `.shape`
Třídě `DataFrame` a `Series` přidejte vlastnost `.shape`, která pomoci tuple reprezentuje rozměry. Vlastnost se bude po každém volání přepočítávat (použíjte dekorátor `@property`).

```python
from data.series import Series
from data.index import Index
from data.dataframe import DataFrame


users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

salaries = Series([20000, 300000, 20000, 50000], index=users)
names = Series(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"], index=users)
cash_flow = Series([-100, 10000, -2000, 1100], index=users)

assert cash_flow.shape == (4, )

data = DataFrame([names, salaries, cash_flow], columns=Index(["names", "salary", "cash flow"]))

assert data.shape == (4, 3)
```

## Metody `.from_csv(text, separator=",")`
Implementujte class metody `DataFrame.from_csv(text, separator=",")` a `Series.from_csv(text, separator=",")` umožňující vytvořit odpovídající třídy na základě řetězce hodnot oddělených separátorem. Na rozdělení textu na jednotlivé řádky použíjte `text.splitlines()`.

Hodnoty vždy reprezenrujte jako řetězec, nepřevádějte je na čísla nebo jiné datové typy.

```python
from data.series import Series

input_text = """user 1,user 2,user 3,user 4
Lukas Novak,Petr Pavel,Pavel Petr,Ludek Skocil
"""

data = Series.from_csv(input_text)
assert data.index.labels == ["user 1", "user 2", "user 3", "user 4"]
assert data.values == ["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"]
```

```python
from data.dataframe import DataFrame

input_text=""",names,salary,cash flow
user 1,Lukas Novak,20000,-100
user 2,Petr Pavel,300000,10000
user 3,Pavel Petr,20000,-2000
user 4,Ludek Skocil,50000,1100"""

data = DataFrame.from_csv(text=input_text)

assert data.columns.labels == ["names", "salary", "cash flow"]

assert list(data.values[0].values) == list(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"])
assert data.values[0].index.labels == ["user 1", "user 2", "user 3", "user 4"]
assert list(data.values[1].values) == list(["20000", "300000", "20000", "50000"])
assert data.values[1].index.labels == ["user 1", "user 2", "user 3", "user 4"]
assert list(data.values[2].values) == list(["-100", "10000", "-2000", "1100"]))
assert data.values[2].index.labels == ["user 1", "user 2", "user 3", "user 4"]

# nezapomeňte, že přetypování na čísla lze řešit následovně (součet všech platů)
data.get("salary").apply(int).sum()
```

## Metody `__str__` a `__repr__` pro třídy `Series` a `DataFrame`

```python
from data.series import Series

users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")
salaries = Series([20000, 300000, 20000, 50000], index=users)
```

Očekávaný výstup `print(salaries)` a `repr(salaries)`. Mezi popis a hodnotu vkládejte tabulátor (`\t`).

```
user 1  20000
user 2  300000
user 3  20000
user 4  50000
```

V případě třídy `DataFrame` bude metoda `__repr__` a `__str__` jednoduší:

```
DataFrame(2, 4)
```

Kde `2` (počet řádků) a `4` jsou rozměry dataframu.

## Series operace
Třídě `Series` implementujte následující operace. Veškeré operace pracují po prvcících, výsledkem je vždy nová instance `Series`. Pokud vstupní instance nebudou mít stejnou délky, vyvolejte `ValueError`.

```
__add__ # chování +
__sub__ # chování -
__mul__ # chování *
__truediv__ # chování /
__floordiv__ # chování //
__mod__ # chování %
__pow__ # chování ** nebo pow()
```

Metody implementujte pomoci pomocné metody `Series._apply_operator(self, other, operator)`, která využívá modul `operator` https://docs.python.org/3/library/operator.html. Sčítání pak například tedy můžeme realizovat jako:

```python
import operator

...
self._apply_operator(self, other, operator.add)
...
```

Dále implementujte metodu `__round__(self, precision)` umožňující použití vestavěné funkce `round(number, precision)`. Výsledkem je opět nová instance `Series`. Dokážete použít metodu `Series.apply(self, func)`?

## Lokální testování
Funkčnost řešení ověříte následujícím příkazem:

```bash
pytest
```