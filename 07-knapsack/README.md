# Fibonacciho posloupnost

Fibonacciho posloupnost je dána rekurzivním předpisem:

$$fib(n) = fib(n − 1) + fib(n − 2)$$
$$fib(0) = 0$$
$$fib(1) = 1$$

1. Implementujme rekurzivní výpočet fibonacciho čísla podle předpisu (top-down).

```python
def fib(n: int) -> int:
    pass
```

Pokud zkusíme program spustit, zjistíme, že pro zvětšující se n je výpočet čísla velice neefektivní. Z výpočtového stromu je patrné, že počítáme stejnou věc několikrát, což vede na velice neefektivní výpočet.

K vypočítání n-tého členu Fibonacciho posloupnosti, můžeme využít rekurzi. Tento postup ale
není optimální, protože budeme stejné části počítat vícekrát, jak ukazuje následující strom řešení:


![Výpočet n-tého čísla fibonacciho posloupnosti](img/tree.png)

Algoritmus můžeme navrhnout efektivněji, když si budeme ukládat mezivýsledky.

2. Vyhledáme část výpočtu, která se opakuje a pokusíme se jí identifikovat. V našem případě je možné použít číslo, které podstrom rozvíjí. Při prvním výpočtu si můžeme výpočet uložit a příště už jej nepočítat.

3. Implementujme rekurzivní výpočet fibonacciho čísla s pamětí předchozích výpočtů (top-down + cache).

```python
def fib_mem(n: int, lookup: dict[int, int]) -> int:
```

4. Porovnejme rychlost výpočtu obou implementací. Porovnejte počet volání funkce s cache a bez cache.

5. Implementujte výpočet fibonacciho čísla bez rekurze pomocí listu (bottom-up s tabulkou)

6. Implementujte výpočet fibonacciho čísla bez rekurze a bez listu (bottom-up neukládejte celou nepotřebnou historii)

7. Rekurzivní výpočet s cache implementujte pomocí @functools.cache

# Kdo stíhá 

## Mix hudby na párty. Praktické užití dynamického programování

## Zadání
Máte za úkol vytvořit mix hudby o dané maximální délce (CD, hudba na diskotéku), tak abyste zahrnuli co nejvíce dobrých písniček. 
Na vstupu dostanete seznam písniček, jejich délky a hodnocení
(oblíbenost). Vaším cílem je maximalizovat celkové hodnocení (součet hodnocení všech skladeb) a
přitom nepřekročit maximální délku.



## Data
Data jsou uložena v jednoduchém textovém formátu kde na každé řádce jsou údaje o jedné skladbě
kde je uloženo hodnocení a čas ve formátu mm:ss. Implementujme načítání dat. 

```python
def load_data(path: str) -> tuple[list[float], list[int]]:
    values: list[float] = [] # rating
    weights: list[int] = [] # délky v sekundách
    return values, weights
```


## Naivní implementace

Úlohu lze řešit poměrně jednoduše s využitím algoritmu navracení, kdy vyzkoušíme zkrátka
všechny možnosti podobně jako v předchozí úloze. To znamená, vyzkoušíme všechny kombinace
rozhodnutí, kdy každou skladbu buď na mix zařadíme a nebo ne. Složitost takového řešení je tedy
$O(2^n)$ kde n je počet skladeb. Toto řešení ale není efektivní. Jeho nevýhody ukazuje následující strom řešení pro zjednodušený příklad, kde máme tři písničky, všechny jsou čtyři minuty dlouhé a vytváříme osmiminutový mix.

V každém kroku musíme vybrat lepší ze dvou možností, buďto danou skladbu do mixu přidáme,
nebo ne. řešení K(0, 8) znamená že se rozhodujeme o první skladbě a 8 minut do kterých vkládáme.
Skladbu buďto zahrneme K(1, 4) nebo nezahrneme K(1, 8).

![knapsack](img/knapsack.png)

##  Dynamické programování

Na obrázku můžeme vidět, k řešení K(2, 4) se dostaneme různými cestami (různé kombinace předchozích skladeb, mají stejnou délku) a backtracking tedy počítá stejné věci vícekrát (stejně jako
v případě Fibonacciho posloupnosti). S narůstající hloubkou řešení se to bude stávat mnohem
častěji. Když tedy problém vhodně dekomponujeme, můžeme se opakovanému výpočtu vyhnout.
Toho můžeme dosáhnout prostým přidáním ukládání výsledků do backtrackingového řešení. Problém stále řešíme rekurzivně (odshora dolů) jen si zaznamenáváme mezivýsledky pro pozdější
použití.

## Poznámka

Dynamické programování je velice mocná technika. Transformace úlohy pro aplikaci dynamického programování mnohdy není přímočará a identifikovat duplicitní část stavového prostoru úlohy je náročné a analýza úlohy  může vyžadovat nezanedbatelný čas a úsilí. To, jakým způsobem dokážeme úlohu analyzovat a identifikovat v ní opakující se výpočty, navíc je použít pro urychlení výpočtu s minimální paměťovou náročností je to, čeho bychom chtěli dosáhnout. 

# Další cvičení

1. Implementujte hladový algoritmus pro úlohu párty mixu. 
    - změřte rychlost a správnost řešení. 
    - jakou cenu platíme za rychlost/správné řešení
2. Jaké písničky do mixu vlastně zařadit? Z naší implementace víme, jaká bude jeho hodnota, samotné písničky ale nikam neukládáme. 

# Motivace a Další materiály

Příklady, kde se DP používá:
- řetězce
- FFT
- řezání materiálů
- optimální naplnění skladu
- investiční portfolia
- kryptografie (např, Merkle-Hellman)

### Další studijní materiály
- Jak souvisí Dynamické programování se studenou válkou? https://www.youtube.com/watch?v=nmgFG7PUHfo

- Více okolo DP https://www.youtube.com/watch?v=Hdr64lKQ3e4

# Apendix

Další možné řešení (méně intuitivní) odstraňuje rekurzi a staví řešení odspoda nahoru s využitím tabulky. 
To spočívá v dekompozici problému na vzájemně se nepřekrývající podproblémy a jejich využití k řešení celého problému s tím, že řešení podproblémů se ukládá do paměti, protože podproblémy se ve stavovém stromu řešení opakují. 
U dynamického programování řešíme problém ”odspodu” stavového stromu. Stav naší úlohy je dán délkou mixu (obecně kapacitou) a počtem skladeb, které jsme se pokusili na mix umístit. Začneme tedy odspodu řešit úlohu. pokud je kapacita, nebo počet skladeb nulový, celkové hodnocení je zjevně také 0, dále pro ostatní případy, můžeme vždy aktuální skladbu buď přidat nebo nepřidat. 
Vybíráme maximum. Na pozici $i$, $j$ máme tedy uložené maximální hodnocení mixu z prvních $i$ skladeb, při celkové délce $j$. Když se rozhodujeme, jestli i-tou skladbu přidat vybíráme maximum ze dvou možností:

1. hodnota $K(i − 1, j)$ – skladbu nepřidáme, hodnocení je stejné jako pro předchozí hodnotu $i$
2. hodnota $K(i − 1, j − d_i + h_i)$ – skladbu předáme. celkové hodnocení se zvýší o hodnocení aktuální skladby hi ale obsadíme $d_i$ minut – přičítáme k nejvyššímu hodnocení s nižší maximální délkou o $d_i$.

Na konci hodnota v poslední buňce tabulky je naše řešení. Vlastně máme řešení pro všechny možné
maximální délky od jedné až do N minut.
![knapsack tabulkou](img/knapsack_tab.png)


