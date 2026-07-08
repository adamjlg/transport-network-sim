from typing import Optional
from dataclasses import dataclass, field
from typing import List

@dataclass
class Train:
    id: str
    route: List[str]
    start_time: int
    dwell: int = 1
    route_index: int = 0
    ready_time: int = field(init=False)
    delay: int = 0
    status: str = 'waiting_to_depart'
    completed: bool = False

    def __post_init__(self):
        self.ready_time = self.start_time

    def current_node(self) -> str:
        return self.route[self.route_index]

    def next_node(self) -> str:
        return self.route[self.route_index + 1]

    def at_final_node(self) -> bool:
        return self.route_index >= len(self.route) - 1