
def load_data_file(filepath: str, wanted_year: int) -> list[Person]:
    people : list[Person] = list()
    return people


def count_average_salary(data: list[Person])-> float:
    return 0.0                    

def count_median_salary(data: list[Person]) -> float:
    return 0.0              

def main(input_path: str):
    year = None         
    data = None         
    avg = count_average_salary(data)
    print(f"Průměrný plat v roce {year}  je  {avg}")

    median = count_median_salary(data)
    print(f"Medián v roce {year}  je  {median}")


if __name__ == "__main__":
    data_path = None 
    main(data_path)

