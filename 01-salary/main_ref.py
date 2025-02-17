
import os
import sys

class Person:

    def __init__(self, first:str, last:str, salary:float):
        self.first: str = first
        self.last: str = last
        self.salary: float = salary

    def __str__(self) -> str:
        return f"{self.first} {self.last} {self.salary}"


def load_data_file(filepath: str, wanted_year: int) -> list[Person]:
    people : list[Person] = list()

    with open(filepath, encoding="utf8") as fd:

        for line_fd in fd:
            line = line_fd.replace("\n", "")
            fields = line.split(";")

            if len(fields) != 15:
                print(f"V řádku je nevalidní záznam -- špatný počet polí\n{line}\n", len(fields), file=sys.stderr)
                continue

            first_s = fields[2]
            last_s = fields[3]
            year_s = fields[12]
            salary_s = fields[14]

            if not year_s.isnumeric():
                print(f"V řádku je nevalidní záznam -- Očekávám číselnou hodnotu\n{line}\n{year_s}", file=sys.stderr)
                continue

            year = int(year_s)
            salary = float(salary_s)
            if year == wanted_year:
                s = Person(first_s, last_s, salary)
                people.append(s)

                if len(people) % 10000 == 0:
                    print(f"loaded {len(people)}")

    return people


def count_average_salary(data: list[Person])-> float:

    suma = 0.0
    for d in data:
        suma += d.salary
    return suma / len(data)


def salary_from_person(p: Person) -> float:
    return p.salary


def count_median_salary(data: list[Person]) -> float:

    # Je několik způsobů jak je možné řadit list objektů.
    # sorted_data = sorted(data, key=lambda x: x.salary)
    sorted_data = sorted(data, key=salary_from_person)
    # sorted_data = sorted(data, key=attrgetter('sallary'))

    if len(sorted_data) % 2 == 1:
        return sorted_data[len(data) // 2].salary
    else:
        return (sorted_data[len(data) // 2 - 1].salary + sorted_data[(len(data) // 2)].salary) / 2


def main(input_path: str):

    avg14 = count_average_salary(load_data_file(input_path, 2014))
    avg15 = count_average_salary(load_data_file(input_path, 2015))

    print(f"Prumerna mzda se pro rok 2014 a 2015 změnila z {avg14} na {avg15} to je o {avg15-avg14} Kč" )

    # Vstupujeme do smyčky, kde se ptáme na rok a počítáme průměr a medián
    while True:
        year_s = input("Zdejte rok (year):")
        if not year_s.isnumeric():
            print("Zadejte numerickou hodnotu")
            continue

        year = int(year_s)
        data = load_data_file(input_path, year)
        if len(data) == 0:
            print("Filtrem na rok neprošly žádné osoby")
            continue
        print(f"Načteno datovych vzorků: {len(data)}\n")
        break

    avg = count_average_salary(data)
    print(f"Průměrný plat v roce {year}  je  {avg}")

    median = count_median_salary(data)
    print(f"Medián v roce {year}  je  {median}")


if __name__ == "__main__":

    print("Program počítá průměrný příjem a medián.")

    arguments = sys.argv
    print(f"nacteno parametrů: {len(arguments)} -- {arguments}")

    if len(arguments) != 2:
        print("Program nebyl spuštěn správně. Očekávám jméno souboru\n ")
        sys.exit(1)

    data_path = arguments[1]
    if not os.path.exists(data_path):
        print(f"Soubor {data_path} neexistuje")
        sys.exit(2)

    main(data_path)

