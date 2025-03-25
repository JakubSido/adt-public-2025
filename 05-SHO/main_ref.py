
import random
from collections import deque


class NamedQueue:
    def __init__(self, name: str):
        self.name = name
        self.q: deque = deque()


class ProcessingNode:
    def __init__(
        self,
        name: str,
        period: int,
        source: NamedQueue,
        destination: NamedQueue,
        sigma: float = 0.1,
    ):
        self.name = name
        self.period = period
        self.sigma = period * sigma

        self.source = source
        self.destination = destination

        self.remaining_time = self.next_occur_in()

    def tick(self) -> None:
        if self.remaining_time <= 0:
            self.perform()
            self.remaining_time = self.next_occur_in()

        self.remaining_time -= 1

    def perform(self) -> None:
        if len(self.source.q) > 0:
            item = self.source.q.popleft()
            self.destination.q.append(item)

    def next_occur_in(self) -> int:
        return int(random.gauss(self.period, self.sigma))


class Observer:
    def __init__(self, list_to_observe: list[NamedQueue]):
        self.list_to_observe = list_to_observe

    def take_snapshot(self) -> str:
        state_strings: list[str] = []
        for named_queue in self.list_to_observe:
            state_strings.append(f"{named_queue.name}({len(named_queue.q)})")

        return "->".join(state_strings)

    def print_snapshot(self, time: int) -> None:
        snapshot = self.take_snapshot()
        h = time // (60 * 60)
        m = (time % (60 * 60)) // 60
        s = time % 60
        print(f"{h:02d}:{m:02d}:{s:02d}\t{snapshot}")



def main() -> None:
    pass
    
    people_number = 1000
    people_in_the_city = deque(list(range(people_number)))

    # vytvoříme "frontu" která bude reprezentovat lidi chodící po městě
    street_q = NamedQueue("in_the_streets")
    street_q.q = people_in_the_city

    # vytvoříme fronty pro jednotlivé obslužné prvky v obchodě
    gate_keeper_q = NamedQueue("shop_gate")
    vege_q = NamedQueue("vege_queue")
    cr_q = NamedQueue("final_cr")

    # frontu lidí, co už z obchodu odešli
    done_q = NamedQueue("done")

    day_m = 1 * 60 # střední hodnota
    gate_m = 0 # střední hodnota
    final_m = 2 * 60  # střední hodnota doby obsluhy na pokladně
    vege_m = 10  # střední hodnota doby obsluhy na váze se zeleninou

    usual_day = ProcessingNode("usual_day_generator", day_m, street_q, gate_keeper_q)
    gate_keeper = ProcessingNode("gate_keeper", gate_m, gate_keeper_q, vege_q)
    vege_cr = ProcessingNode("vege_1", vege_m, vege_q, cr_q)
    crs = ProcessingNode("final_crs_1", final_m, cr_q, done_q)

    to_tick: list[ProcessingNode] = [crs, vege_cr, gate_keeper, usual_day]

    observer = Observer([street_q, gate_keeper_q, vege_q, cr_q, done_q])

    for time in range(2 * 60 * 60):
        for te in to_tick:
            te.tick()

        if time % (10) == 0:
            observer.print_snapshot(time)
    


if __name__ == "__main__":
    main()

