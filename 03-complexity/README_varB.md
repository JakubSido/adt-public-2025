## Mikrobenchmark důležitých operací

Již minule jsem říkal, že datová struktura množina je pro některé operace rychlejší, než list.

Dnes si tuto informaci ověříme a pokusíme se pochopit proč tomu tak je.

Na tomto cvičení by mělo být hodně prostoru pro samostatnou práci, doptávání se na otázky na které obvykle není čas a diskutování některých detailů implementace.

### Postup

Začínáme bez předlohy, kód si smíte strukturovat jak chcete, ale pokuste se dbát na to aby byl přehledný.

1. Implementujme funkci `time_in()`, která změří dobu běhu operace `in` nad listem. Předávaný list bude obsahovat prvky `0..5000`. Aby byly časy měřitelné a mohli jsme je vyprůměrovat, tak uděláme `n = 1_000` opakování.
    
	- Existuje více způsobů jak operaci časovat, který je nejlepší a proč?
		- Čas od 1 ledna 1970 v sekundách jako reálné číslo vám poskytne funkce `time.time()` (`import time`).
	- Jak se mění doba běhu v závislosti na vyhledávaném prvku?
	- Funkci upravte tak, aby měřila průměrnou dobu jednoho opakování operace, místo celkového času.

2. Výsledky budou přehlednější, když si vytvoříme graf.

	- Napište funkci, která za pomocí funkce `time_in()` načasuje to samé pro různé velikosti vstupního listu.
		- Data v listu smysluplně pozměňte podle cílové velikosti.
	- Výsledky naskládejte do grafu, využijte knihovnu `plotly`
		- knihovnu nainstalujte příkazem `pip install plotly --user` v terminálu.
		- [příklad použití](https://plotly.com/python/line-charts/index.html#style-line-plots)
	- Změňte vyhledávaný prvek za `-1`.

**Funkce na grafování:**

Pokud si neumíte upravit příklady z dokumentace knihovny pro grafování, tak můžete použít následující funkci.

```python
import plotly.graph_objects as go

def plot_experiments(experiments: dict[str, list[float]], x_axis: list[int]) -> None:
    fig = go.Figure()
	
    for method, timings in experiments.items():
        fig.add_trace(go.Scatter(
            x=x_axis,
            y=timings,
            name=method,
        ))
		
    fig.update_layout(
        yaxis={
            "ticksuffix": "s",
            "title": "Time (seconds)",
        }
    )
	
    fig.write_html("complexity_plot.html")
    fig.show()

# Příklad vstupních dat funkce.
experiments = {
    "in_set": [1.4, 1.3, 2.0, 1.0, 2.0],
    "in_list": [1.3, 1.4, 1.2, 1.5, 1.9]
}
x_axis = [0, 1, 2, 3, 4]

# Použití funkce
plot_experiments(experiments, x_axis)
```


3. Teď je na čase si vyzkoušet porovnat výsledky mezi listem a množinou. Kód upravte tak, aby do grafu vložil jednu řadu pro list a druhou pro množinu.

	- Úpravu by mělo být možné realizovat minimální změnou kódu.
		- Hlavním rozdílem bude tvorba množiny místo listu. Prozatím to realizujte, jak zvládnete.
		- Druhým rozdílem bude type hint funkce. Pokud jste ho vynechali, tak ho doplňte.
	- Pro typování využijte `from collections.abc import Collection`. `Collection` je abstraktní typ, který můžeme procházet (iterovat) a volat nad ním `in`.

4. **Předávání funkcí funkcím.** Kód měření času upravte tak, aby bylo možné jednoduše změnit časovanou operaci.

	- Přidejte `from typing import Callable`. `Callable` je typ, který lze zavolat úplně stejně jako funkci. Funkce jsou `Callable`.
	- Novou hlavičkou funkce `time_in()` bude `time_operation(operation: Callable, num_repeats: int = 10_000) -> float`. Nezapomeňte upravit všechny volání funkce.
	
5. Vyhledávání jiných objektů -- vlastní přepravka.

	- Vytvořte přepravku `Rectangle`, která sestává z celočíselných velikostí svých hran `a` a `b`.
	- Tuto přepravku připravte na vložení do množiny implementací metod `__eq__` a `__hash__`.
		- `def __eq__(self, other: object) -> bool` definuje, které jiné objekty se "rovnají" této instanci
		- `def __hash__(self) -> int` implementuje tzn. hash. Můžeme to chápat jako číslo, které odpovídá objektu. Toto číslo je pro množinu důležité aby uměla objekty uložit.
		- [relevantní diskuze](https://stackoverflow.com/questions/10547343/add-object-into-pythons-set-collection-and-determine-by-objects-attribute)

6. *[Volitelná rozšíření]*

	- Co se stane, když hash bude vždy `0`?
	- Množiny a Slovníky (`dict`) interně fungují pomocí datové struktury `HashMap`. [Krátké video](https://www.youtube.com/watch?v=WEILxTBDy0Y)
<!--	- Ve standarndím balíčku `time` existuje více variant pro měření času. Hlavní z nich jsou:
		- `time.time()` - skutečný čas od January 1, 1970, 00:00:00 (UTC), v sekundách -->

### K čemu to všechno bylo?

Nyní bychom měli mít představu, jak programátoři dělají tzn. Microbenchmarky, tedy extrémní testy malých částí kódu. Microbenchmarky jsou velmi užitečné pro optimalizaci klíčových částí programů. Také jsou ale velmi zrádné a je extrémně lehké udělat chybu, která obrátí výsledky na hlavu.

Zároveň jsme si vytvořili některé intuice ohledně toho, proč používáme různé datové struktury a jak se projeví využití nevhodné datové struktury. Viděli jsme, že algoritmické složitosti se skutečně propisují do praxe a jsou měřitelné.

