from collections import defaultdict
import os
import sys



class Record():
    time:int
    id_cust:int
    ckpt:str
    
    def __init__(self,time:int ,id_cust: int,ckpt:str) -> None:
        self.time = time
        self.id_cust = id_cust
        self.ckpt = ckpt
    


def load_data(data_path:str ,city:str ,shop:str, day="1-Mon") -> dict[str, list[Record]]|None:
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

    city_data: dict[str, list[Record]] = defaultdict(lambda: list())
    print("loading", city)

    return city_data 


def get_passed_set(data : dict[str, list[Record]],key_words:list[str]) -> set[int]:
    """Funkce vrátí množinu zákazníků, kteří prošli alespoň jedním z checkpointů s prefixem předaných jako key_words.
    Do funkce tedy nevstupuje celé jméno checkpointu ale pouze jeho prefix (např. vege místo vege_1).

    Args:
        data (dict[str, list[Record]]): data načtená z datového souboru funkcí load_data 
        key_words (list[str]): prefixové označení checkpointů, které chceme sledovat (např. vege, frui, meat) 

    Returns:
        set[int]: _description_
    """
    customers : set[int] = set()
    return customers
            

def filter_data_time(data :dict[str, list[Record]], cond_time:int) -> dict[str, list[Record]]:
    ret: dict[str, list[Record]] = defaultdict(lambda: list())
    return ret
         
def get_q_size(data :dict[str, list[Record]], seconds:int) -> int:   
    queue : set[int] = set()   
    return len(queue)
    

def histogram(data :dict[str, list[Record]]):
    pass

def main(data_dir: str):
    
    data = None

if __name__ == "__main__":
    datadir = ""
    main(datadir)
