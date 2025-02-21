from collections import defaultdict
import os
import sys


class Record():
    time:int
    id_cost:int
    ckpt:str

    def __init__(self,time:int ,id_cost: int,ckpt:str) -> None:
        self.time = time
        self.id_cost = id_cost
        self.ckpt = ckpt


    def __repr__(self) -> str:
        return f"id:{self.id_cost} time:{self.time}"



def load_data(data_path:str ,city:str, shop:str, day:str="1-Mon") -> dict[str, list[Record]]|None:
    """ Funkce načte data z daného souboru a vrátí je jako slovník.
    Klíčem je název checkpointu a hodnotou je list záznamů.

    Args:
        data_path (str): cesta k adresáři se všemi daty
        city (str): název města, které chceme načíst
        shop (str): název obchodu, který chceme načíst
        day (str, optional): Konkrétní den, který chceme načíst. Defaults to "1-Mon".

    Returns:
        dict[str, list[Record]]|None: slovník s načtenými daty nebo None pokud soubor neexistuje  
    """

    # pozn. Můžeme použít default dict, nebo použít běžný slovník a při přidání nového záznamu 
    # vždy zkontrolovat, zda klíč již existuje, případně inicializovat prázdný list

    city_data: dict[str, list[Record]] = dict()
    # city_data: dict[str, list[Record]] = defaultdict(list)

    print("loading", city)

    
    shop_path = os.path.join(data_path, city, day, f"{shop}.txt")
    if not os.path.exists(shop_path):
        print("soubor neexistuje", shop_path)
        return None

    with open(shop_path, 'r', encoding="utf8") as fd:
        _ = fd.readline() # skip header

        lines = fd.readlines()
        for line in lines:
            line = line.replace("\n", "") # remove newline character

            spl = line.split(";")
            try:
                r = Record(int(spl[0]),int(spl[2]),spl[1])
                key = f"{r.ckpt}"
                if key not in city_data:
                    city_data[key] = list() 
                city_data[key].append(r)
            except ValueError as e:
                print("chyba v souboru ValueError neocekavana hodnota",shop_path,"\n",line)
                continue
            except IndexError as e:
                print("chyba v souboru IndexError neocekavany pocet hodnot",shop_path,"\n",line)
                continue
    
    return city_data


def get_passed_set(data : dict[str, list[Record]], key_words:list[str]) -> set[int]:
    """Funkce vrátí množinu zákazníků, kteří prošli alespoň jedním z checkpointů s prefixem předaných jako key_words.
    Do funkce tedy nevstupuje celé jméno checkpointu ale pouze jeho prefix (např. vege místo vege_1).

    Args:
        data (dict[str, list[Record]]): data načtená z datového souboru funkcí load_data 
        key_words (list[str]): prefixové označení checkpointů, které chceme sledovat (např. vege, frui, meat) 

    Returns:
        set[int]: Funkce vrací množinu identifikačních čísel zákazníků.
    """
    customers : set[int] = set()
    
    for k,d in data.items():
        # Díky prefixování klíče checkpointu (vege_1, vege_2, ...) můžeme snadno zjistit, zda checkpoint obsahuje některé z klíčových slov.
        # Díky tomu můžeme např. snadno posčítat zákazníky, kteří prošli jakýmkoli vege_X (X je identifikátor pokladny pro zeleninu)

        d_ckpt_gen = k.split("_")[0]  # vege_1 -> vege
        if d_ckpt_gen in key_words:
            for r in d:
                customers.add(r.id_cost)
    
    return customers

def filter_data_time(data :dict[str, list[Record]], cond_time:int) -> dict[str, list[Record]]:
    ret: dict[str, list[Record]] = defaultdict(list)
    
    for k,v in data.items():
        for r in v:
            if int(r.time) > cond_time:
                break 
            ret[k].append(r)
    
    return ret

def get_q_size(data :dict[str, list[Record]], seconds:int) -> int:
    queue : set[int] = set()
    
    filtered_data = filter_data_time(data,seconds)

    key_words = ["vege","frui","meat"]
    first = get_passed_set(filtered_data,key_words)

    key_words = ["final-crs"]
    second = get_passed_set(filtered_data,key_words)

    queue = first.difference(second)
    
    return len(queue)


def histogram(data :dict[str, list[Record]]) -> None:
    pass
    

    for m in range(0,24*60,10):
        seconds = m*60

        q_size = get_q_size(data,seconds)

        h = m // 60
        mi = m % 60
        print(f"{h}:{mi} -- {q_size}  ")
    

def main(data_dir: str) -> None:

    data = None
    
    while True:
        city = input("Zadejte město (např Plzeň): ")
        shop = input("Zadejte jméno souboru obchodu: (např shop_a -- stejné jako jméno souboru): ")
        data = load_data(data_dir, city,shop)
        if data is None:
            print("zadna data nebyla nactena")
            continue
        histogram(data)
    

if __name__ == "__main__":
    datadir = ""
    
    argv = sys.argv
    if len(argv) < 2:
        print("Usage: python main.py <data_dir>")
        sys.exit(1)

    datadir = argv[1]

    if not os.path.exists(datadir):
        print("složka z daty neexistuje")

    
    main(datadir)

